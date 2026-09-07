"""
Unit and Integration Tests for Milestone 4:
HL7 FHIR Release 4 Interoperability Exporter & Automated Specialist Referral Generator.
"""

import uuid
import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.models.analysis import Analysis
from app.models.user import User
from app.services.fhir_exporter import build_fhir_bundle, generate_specialist_referral_letter
from app.db.session import SessionLocal

client = TestClient(app)


def test_build_fhir_bundle_composition_and_ontology():
    user = User(id=42, username="oncologist_rao", full_name="Dr. Rao", role="clinician", email="rao@hospital.org")
    analysis = Analysis(
        id=101,
        patient_identifier="PT-FHIR-77",
        prediction="cancer",
        confidence=0.94,
        uncertainty=0.012,
        risk_score=0.75,
        lesion_site="lateral_tongue",
        triage_tier="Tier 3 // High Suspicion (Urgent Biopsy Referral)",
        telemetry_data='{"diameter_mm": 24.5, "surface_area_mm2": 310.0, "border_irregularity_score": 1.55}',
        timestamp=datetime.datetime.utcnow(),
        biopsy_proven=False
    )

    bundle = build_fhir_bundle(analysis, user)

    # 1. Bundle Structural Conformance
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert len(bundle["entry"]) >= 4

    resource_types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert "Patient" in resource_types
    assert "Practitioner" in resource_types
    assert "Observation" in resource_types
    assert "DiagnosticReport" in resource_types
    assert "ServiceRequest" in resource_types  # Tier 3 cancer requires ServiceRequest referral

    # 2. Patient Resource
    patient_res = next(e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "Patient")
    assert patient_res["identifier"][0]["value"] == "PT-FHIR-77"

    # 3. Observation SNOMED & LOINC Codes
    obs_res = [e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "Observation"]
    loinc_codes = []
    for obs in obs_res:
        for c in obs["code"]["coding"]:
            loinc_codes.append(c["code"])
    assert "72170-4" in loinc_codes  # LOINC Oral cavity photography study
    assert "21889-1" in loinc_codes  # LOINC Size of tumor

    # 4. ServiceRequest Urgency
    service_req = next(e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "ServiceRequest")
    assert service_req["priority"] == "urgent"


def test_specialist_referral_letter_generator():
    user = User(id=88, username="dr_sharma", full_name="Dr. Sunita Sharma", role="clinician", email="sharma@cancercenter.org")
    analysis = Analysis(
        id=202,
        patient_identifier="PT-REF-09",
        prediction="cancer",
        confidence=0.88,
        uncertainty=0.009,
        risk_score=0.80,
        lesion_site="floor_of_mouth",
        triage_tier="Tier 3 // High Suspicion",
        telemetry_data='{"diameter_mm": 18.0, "surface_area_mm2": 210.0, "border_irregularity_score": 1.48}',
        timestamp=datetime.datetime.utcnow()
    )

    letter = generate_specialist_referral_letter(analysis, user)
    assert letter["referral_reference_id"] == "REF-ONC-2026-0202"
    assert "URGENT" in letter["urgency"]
    assert letter["referring_clinician"]["name"] == "Dr. Sunita Sharma"
    assert letter["patient"]["mrn_identifier"] == "PT-REF-09"
    assert letter["diagnostic_findings"]["calibrated_diameter_mm"] == 18.0
    assert "Incisional scalpel biopsy" in letter["biopsy_directive"]


def test_fhir_and_referral_api_endpoints():
    uid = uuid.uuid4().hex[:6]
    username = f"fhir_doc_{uid}"
    pwd = "FhirPassword123!"

    # 1. Register & Login
    reg = client.post("/register", json={"username": username, "password": pwd, "email": f"{username}@clinic.org"})
    assert reg.status_code == 201
    login = client.post("/login", data={"username": username, "password": pwd})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Insert test specimen
    db = SessionLocal()
    clinician = db.query(User).filter(User.username == username).first()
    test_specimen = Analysis(
        user_id=clinician.id,
        patient_identifier=f"PT-FHIR-{uid}",
        prediction="cancer",
        confidence=0.96,
        uncertainty=0.007,
        risk_score=0.82,
        lesion_site="lateral_tongue",
        triage_tier="Tier 3 // High Suspicion (Urgent Biopsy Referral)",
        image_filename="fhir_specimen.jpg",
        telemetry_data='{"diameter_mm": 22.0, "surface_area_mm2": 280.0, "border_irregularity_score": 1.6}'
    )
    db.add(test_specimen)
    db.commit()
    db.refresh(test_specimen)
    specimen_id = test_specimen.id
    db.close()

    # 3. Test GET /analyses/{id}/fhir
    fhir_res = client.get(f"/analyses/{specimen_id}/fhir", headers=headers)
    assert fhir_res.status_code == 200
    fhir_data = fhir_res.json()
    assert fhir_data["resourceType"] == "Bundle"
    assert fhir_data["type"] == "collection"

    # 4. Test GET /analyses/{id}/referral
    ref_res = client.get(f"/analyses/{specimen_id}/referral", headers=headers)
    assert ref_res.status_code == 200
    ref_data = ref_res.json()
    assert f"REF-ONC-2026-{specimen_id:04d}" == ref_data["referral_reference_id"]
    assert "URGENT" in ref_data["urgency"]
    assert ref_data["patient"]["mrn_identifier"] == f"PT-FHIR-{uid}"
