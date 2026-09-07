import pytest
import numpy as np
from PIL import Image

from app.services.vision_pipeline import (
    compute_lesion_segmentation,
    analyze_vital_stain,
    execute_dual_stage_pipeline,
    LesionSpatialTelemetry
)

def test_compute_lesion_segmentation_fallback():
    # Uniform gray image should trigger the synthetic central ROI fallback
    img = Image.new("RGB", (224, 224), color=(180, 150, 150))
    detected, center, diameter_mm, area_mm2, irregularity, contour = compute_lesion_segmentation(img)
    
    assert detected is False
    assert center == (50.0, 50.0)
    assert diameter_mm == 12.0
    assert len(contour) > 0

def test_compute_lesion_segmentation_erythematous_patch():
    # Create image with bright red/erythematous lesion in top-right quadrant
    arr = np.full((224, 224, 3), 120, dtype=np.uint8)
    arr[40:100, 130:190, 0] = 240  # High red
    arr[40:100, 130:190, 1] = 40   # Low green (high erythema)
    arr[40:100, 130:190, 2] = 40
    
    img = Image.fromarray(arr)
    detected, (cx, cy), diameter_mm, area_mm2, irregularity, contour = compute_lesion_segmentation(img, distance_mm=50.0)
    
    assert detected is True
    # Center should be biased toward upper right (cx > 50%, cy < 50%)
    assert cx > 50.0
    assert cy < 50.0
    assert diameter_mm > 0.0
    assert area_mm2 > 0.0
    assert irregularity >= 1.0
    assert len(contour) > 5

def test_analyze_vital_stain_none():
    present, abnormal = analyze_vital_stain(None)
    assert present is False
    assert abnormal is False

def test_analyze_vital_stain_normal_vs_abnormal():
    # Normal oral mucosa (pinkish/red, balanced blue)
    normal_img = Image.new("RGB", (100, 100), color=(180, 100, 110))
    pres, abn = analyze_vital_stain(normal_img)
    assert pres is True
    assert abn is False

    # Abnormal toluidine blue uptake (deep purple/blue)
    dysplastic_img = Image.new("RGB", (100, 100), color=(30, 40, 220))
    pres_abn, is_abn = analyze_vital_stain(dysplastic_img)
    assert pres_abn is True
    assert is_abn is True

def test_execute_dual_stage_pipeline_telemetry():
    img = Image.new("RGB", (224, 224), color=(160, 120, 120))
    pred_class, conf, unc, qual, telemetry = execute_dual_stage_pipeline(
        white_light_img=img,
        vital_stain_img=None,
        distance_mm=50.0,
        is_cross_polarized=True
    )

    assert pred_class in ["cancer", "non_cancer", "uncertain"]
    assert 0.0 <= conf <= 1.0
    assert isinstance(telemetry, LesionSpatialTelemetry)
    assert telemetry.optical_cross_polarized is True
    assert telemetry.vital_stain_present is False
    assert len(telemetry.contour_points) > 0
