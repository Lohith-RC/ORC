import io
import uuid
import pytest
from PIL import Image
import numpy as np
import torch
from fastapi.testclient import TestClient

from app.main import app
from app.services.ml_engine import get_model, inference_transform
from app.services.xai_cam import GradCAMPlusPlus, convert_cam_to_base64_png, compute_activation_lesion_concordance
from app.services.optical_normalization import apply_reinhard_mucosal_normalization, detect_and_suppress_specular_glare
from app.services.multimodal_fusion import evaluate_multimodal_ordinal_triage

client = TestClient(app)

def test_reinhard_normalization_preserves_dimensions_and_type():
    img = Image.new("RGB", (64, 64), color=(210, 140, 130))
    norm = apply_reinhard_mucosal_normalization(img)
    assert norm.size == (64, 64)
    assert norm.mode == "RGB"

def test_glare_suppression_detects_saturated_glare():
    # Create image with a bright white glare patch (saliva reflection)
    arr = np.full((100, 100, 3), 140, dtype=np.uint8)
    arr[40:60, 40:60] = 255 # Blown out specular white
    img = Image.fromarray(arr)
    
    clean_img, telemetry = detect_and_suppress_specular_glare(img)
    assert telemetry["glare_percentage"] > 0.0
    assert "optical_uniformity_score" in telemetry
    assert clean_img.size == (100, 100)

def test_gradcam_plus_plus_generates_bounded_heatmap():
    model = get_model()
    cam_engine = GradCAMPlusPlus(model, model.res_features[-1])
    
    dummy_img = Image.new("RGB", (224, 224), color=(180, 100, 100))
    tensor = inference_transform(dummy_img).unsqueeze(0)
    
    heatmap = cam_engine.generate_heatmap(tensor, target_class=0)
    cam_engine.remove_hooks()
    
    assert heatmap.shape == (224, 224)
    assert np.all(heatmap >= 0.0)
    assert np.all(heatmap <= 1.0)
    
    b64 = convert_cam_to_base64_png(heatmap)
    assert b64.startswith("data:image/png;base64,")

def test_lesion_concordance_calculation():
    cam_array = np.zeros((224, 224), dtype=np.float32)
    # Hot spot at center
    cam_array[80:140, 80:140] = 0.9
    
    # Matching contour at center
    contour = [(40.0, 40.0), (60.0, 40.0), (60.0, 60.0), (40.0, 60.0)]
    score, alert = compute_activation_lesion_concordance(cam_array, contour, canvas_size=(224, 224))
    
    assert 0.0 <= score <= 1.0
    assert isinstance(alert, str)

def test_4_class_ordinal_triage_distribution():
    res = evaluate_multimodal_ordinal_triage(
        binary_confidence=0.92,
        binary_prediction="cancer",
        clinical_risk_score=0.80,
        border_irregularity=1.75,
        diameter_mm=28.0,
        vital_stain_abnormal=True,
        lesion_site="lateral_tongue"
    )
    
    assert res.predicted_class in ["normal", "benign", "opmd", "malignant"]
    probs = res.class_probabilities
    assert set(probs.keys()) == {"normal", "benign", "opmd", "malignant"}
    total_p = sum(probs.values())
    assert 0.99 <= total_p <= 1.01 # Sums to 1.0 within floating point rounding
    assert 0.0 <= res.ordinal_severity_score <= 3.0
    assert res.triage_urgency in ["ROUTINE", "MONITOR", "ELEVATED", "CRITICAL"]

def test_predict_endpoint_returns_extended_clinical_telemetry():
    uid = uuid.uuid4().hex[:6]
    username = f"xai_doc_{uid}"
    pwd = "ValidPassword123!"
    
    reg = client.post("/register", json={"username": username, "password": pwd, "email": f"{username}@test.org"})
    assert reg.status_code == 201
    login = client.post("/login", data={"username": username, "password": pwd})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    img = Image.new("RGB", (224, 224), color=(160, 90, 80))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    
    res = client.post(
        "/predict",
        headers=headers,
        files={"file": ("specimen.jpg", buf, "image/jpeg")},
        data={
            "patient_identifier": "XAI-TEST-001",
            "lesion_site": "buccal_mucosa",
            "age": "55",
            "tobacco_use": "true",
            "betel_nut": "true"
        }
    )
    assert res.status_code == 200
    data = res.json()
    
    # Assert new Phase 1-4 capabilities exist in payload
    assert "xai_explainability" in data
    assert "optical_quality" in data
    assert "ordinal_triage" in data
    
    assert data["xai_explainability"]["gradcam_heatmap_base64"].startswith("data:image/png;base64,")
    assert "concordance_score" in data["xai_explainability"]
    assert "optical_uniformity_score" in data["optical_quality"]
    assert data["ordinal_triage"]["predicted_class"] in ["normal", "benign", "opmd", "malignant"]
    assert "ordinal_severity_score" in data["ordinal_triage"]
