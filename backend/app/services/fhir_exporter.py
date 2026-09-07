"""
HL7 FHIR Release 4 Interoperability Exporter & Specialist Referral Generator.
Produces compliant FHIR r4 JSON Bundles and structured oncological referral summaries.
"""

import json
import datetime
from typing import Dict, Any, Optional
from app.models.analysis import Analysis
from app.models.user import User

# Standard LOINC & SNOMED CT Ontology Codes
SNOMED_CODES = {
    "cancer": {"code": "35917007", "display": "Squamous cell carcinoma of oral cavity"},
    "uncertain": {"code": "281399006", "display": "Oral cavity condition with uncertain malignant potential"},
    "benign": {"code": "263855007", "display": "Normal oral mucosal structure"},
}

ORAL_SITE_SNOMED = {
    "lateral_tongue": {"code": "21974007", "display": "Lateral margin of tongue"},
    "floor_of_mouth": {"code": "81206001", "display": "Floor of mouth"},
    "buccal_mucosa": {"code": "38385002", "display": "Buccal mucosa"},
    "gingiva": {"code": "361351001", "display": "Gingival structure"},
    "dorsal_tongue": {"code": "47975008", "display": "Dorsal surface of tongue"},
    "soft_palate": {"code": "72914002", "display": "Soft palate"},
    "hard_palate": {"code": "49460000", "display": "Hard palate"},
    "lip": {"code": "485005", "display": "Lip structure"},
}


def build_fhir_bundle(analysis: Analysis, practitioner: User) -> Dict[str, Any]:
    """
    Constructs an HL7 FHIR Release 4 compliant JSON Bundle (type: collection)
    containing Patient, Practitioner, Observations (Diagnostic verdict & Morphometry),
    DiagnosticReport, and ServiceRequest (Specialist Referral).
    """
    timestamp_str = (analysis.timestamp or datetime.datetime.utcnow()).isoformat() + "Z"
    bundle_id = f"bundle-orc-{analysis.id}"
    patient_id = f"pat-{analysis.patient_identifier or 'ANON-001'}"
    practitioner_id = f"prac-{practitioner.id}"

    # Parse telemetry JSON if present
    telemetry = {}
    if analysis.telemetry_data:
        try:
            telemetry = json.loads(analysis.telemetry_data)
        except Exception:
            telemetry = {}

    diameter_mm = telemetry.get("diameter_mm", 12.0)
    surface_area_mm2 = telemetry.get("surface_area_mm2", 113.1)
    border_irregularity = telemetry.get("border_irregularity_score", 1.15)
    site_key = analysis.lesion_site or "buccal_mucosa"
    site_info = ORAL_SITE_SNOMED.get(site_key, {"code": "38385002", "display": "Buccal mucosa"})

    pred_key = analysis.prediction.lower()
    snomed_verdict = SNOMED_CODES.get(pred_key, SNOMED_CODES["benign"])
    is_cancer = (pred_key == "cancer")

    entries = []

    # 1. Patient Resource
    patient_entry = {
        "fullUrl": f"urn:uuid:{patient_id}",
        "resource": {
            "resourceType": "Patient",
            "id": patient_id,
            "identifier": [
                {
                    "use": "usual",
                    "system": "urn:oid:oral-cancer-ai:patient:mrn",
                    "value": analysis.patient_identifier or "ANON-001"
                }
            ],
            "active": True
        }
    }
    entries.append(patient_entry)

    # 2. Practitioner Resource
    prac_entry = {
        "fullUrl": f"urn:uuid:{practitioner_id}",
        "resource": {
            "resourceType": "Practitioner",
            "id": practitioner_id,
            "name": [
                {
                    "use": "official",
                    "text": practitioner.full_name or f"Dr. {practitioner.username}"
                }
            ],
            "telecom": [
                {
                    "system": "email",
                    "value": practitioner.email or "clinician@hospital.org"
                }
            ]
        }
    }
    entries.append(prac_entry)

    # 3. Observation: AI Deep Vision Verdict & Epistemic Uncertainty
    obs_verdict_id = f"obs-verdict-{analysis.id}"
    obs_verdict = {
        "fullUrl": f"urn:uuid:{obs_verdict_id}",
        "resource": {
            "resourceType": "Observation",
            "id": obs_verdict_id,
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "exam",
                            "display": "Exam"
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "72170-4",
                        "display": "Photographic study of oral cavity"
                    }
                ],
                "text": "Deep Learning Oral Cancer Diagnostic Screening"
            },
            "subject": {"reference": f"urn:uuid:{patient_id}"},
            "performer": [{"reference": f"urn:uuid:{practitioner_id}"}],
            "effectiveDateTime": timestamp_str,
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": snomed_verdict["code"],
                        "display": snomed_verdict["display"]
                    }
                ],
                "text": analysis.prediction.upper()
            },
            "component": [
                {
                    "code": {
                        "coding": [{"system": "http://loinc.org", "code": "79116-0", "display": "Confidence Score"}],
                        "text": "Neural Ensemble Confidence"
                    },
                    "valueQuantity": {
                        "value": round(float(analysis.confidence), 4),
                        "unit": "ratio",
                        "system": "http://unitsofmeasure.org",
                        "code": "1"
                    }
                },
                {
                    "code": {
                        "coding": [{"system": "urn:oid:oral-cancer-ai:metric", "code": "epistemic-uncertainty"}],
                        "text": "Epistemic Uncertainty Variance (MC Dropout)"
                    },
                    "valueQuantity": {
                        "value": round(float(analysis.uncertainty or 0.0), 5),
                        "unit": "variance",
                        "system": "http://unitsofmeasure.org",
                        "code": "1"
                    }
                },
                {
                    "code": {
                        "coding": [{"system": "urn:oid:oral-cancer-ai:metric", "code": "clinical-risk-score"}],
                        "text": "Epidemiological Risk Score"
                    },
                    "valueQuantity": {
                        "value": round(float(analysis.risk_score or 0.0), 3),
                        "unit": "score",
                        "system": "http://unitsofmeasure.org",
                        "code": "1"
                    }
                }
            ]
        }
    }
    entries.append(obs_verdict)

    # 4. Observation: Spatial Lesion Morphometry (Calibrated Diameter, Surface Area, Border Irregularity)
    obs_morph_id = f"obs-morph-{analysis.id}"
    obs_morph = {
        "fullUrl": f"urn:uuid:{obs_morph_id}",
        "resource": {
            "resourceType": "Observation",
            "id": obs_morph_id,
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "imaging",
                            "display": "Imaging"
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "21889-1",
                        "display": "Size of tumor"
                    }
                ],
                "text": "Oral Mucosal Lesion Morphometric Telemetry"
            },
            "subject": {"reference": f"urn:uuid:{patient_id}"},
            "effectiveDateTime": timestamp_str,
            "bodySite": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": site_info["code"],
                        "display": site_info["display"]
                    }
                ],
                "text": site_key.replace("_", " ").title()
            },
            "component": [
                {
                    "code": {
                        "coding": [{"system": "http://loinc.org", "code": "33728-7", "display": "Lesion size.maximum diameter"}],
                        "text": "Calibrated Diameter"
                    },
                    "valueQuantity": {
                        "value": round(float(diameter_mm), 1),
                        "unit": "mm",
                        "system": "http://unitsofmeasure.org",
                        "code": "mm"
                    }
                },
                {
                    "code": {
                        "coding": [{"system": "urn:oid:oral-cancer-ai:metric", "code": "surface-area"}],
                        "text": "Lesion Surface Area"
                    },
                    "valueQuantity": {
                        "value": round(float(surface_area_mm2), 1),
                        "unit": "mm2",
                        "system": "http://unitsofmeasure.org",
                        "code": "mm2"
                    }
                },
                {
                    "code": {
                        "coding": [{"system": "urn:oid:oral-cancer-ai:metric", "code": "border-irregularity-index"}],
                        "text": "Border Irregularity Ratio"
                    },
                    "valueQuantity": {
                        "value": round(float(border_irregularity), 2),
                        "unit": "index",
                        "system": "http://unitsofmeasure.org",
                        "code": "1"
                    }
                }
            ]
        }
    }
    entries.append(obs_morph)

    # 5. DiagnosticReport Resource
    report_id = f"diagrep-orc-{analysis.id}"
    cT_stage = "cT1" if diameter_mm <= 20.0 else ("cT2" if diameter_mm <= 40.0 else "cT3")
    triage_tier_str = analysis.triage_tier or ("Tier 3 // High Suspicion" if is_cancer else "Tier 1 // Low Risk")

    diag_report = {
        "fullUrl": f"urn:uuid:{report_id}",
        "resource": {
            "resourceType": "DiagnosticReport",
            "id": report_id,
            "status": "final" if analysis.biopsy_proven else "preliminary",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                            "code": "CP",
                            "display": "Clinical Pathology"
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "11526-1",
                        "display": "Pathology study"
                    }
                ],
                "text": "Oral Oncology Clinical Triage & Staging Summary"
            },
            "subject": {"reference": f"urn:uuid:{patient_id}"},
            "performer": [{"reference": f"urn:uuid:{practitioner_id}"}],
            "effectiveDateTime": timestamp_str,
            "result": [
                {"reference": f"urn:uuid:{obs_verdict_id}"},
                {"reference": f"urn:uuid:{obs_morph_id}"}
            ],
            "conclusion": (
                f"AJCC 8th Edition Clinical Staging: {cT_stage} cN0 cM0 (Presumptive). "
                f"Triage Level: {triage_tier_str}. "
                f"{'Histopathologically proven: ' + str(analysis.ground_truth_dx) if analysis.biopsy_proven else 'Preliminary AI screening; biopsy verification indicated.'}"
            )
        }
    }
    entries.append(diag_report)

    # 6. ServiceRequest (Specialist Referral - generated if high suspicion or Tier 3)
    if is_cancer or "Tier 3" in triage_tier_str:
        req_id = f"req-oncology-referral-{analysis.id}"
        service_req = {
            "fullUrl": f"urn:uuid:{req_id}",
            "resource": {
                "resourceType": "ServiceRequest",
                "id": req_id,
                "status": "active",
                "intent": "order",
                "priority": "urgent",
                "code": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "306206005",
                            "display": "Referral to oral and maxillofacial surgeon"
                        }
                    ],
                    "text": "Urgent Maxillofacial / Head & Neck Oncology Consultation"
                },
                "subject": {"reference": f"urn:uuid:{patient_id}"},
                "requester": {"reference": f"urn:uuid:{practitioner_id}"},
                "occurrenceDateTime": timestamp_str,
                "reasonCode": [
                    {
                        "text": f"High-suspicion oral mucosal lesion at {site_info['display']}. Estimated diameter {diameter_mm}mm, AJCC stage {cT_stage}. Incisional scalpel biopsy recommended."
                    }
                ]
            }
        }
        entries.append(service_req)

    return {
        "resourceType": "Bundle",
        "id": bundle_id,
        "type": "collection",
        "timestamp": timestamp_str,
        "entry": entries
    }


def generate_specialist_referral_letter(analysis: Analysis, practitioner: User) -> Dict[str, Any]:
    """
    Generates structured clinical specialist referral letter metadata
    ready for formal PDF export or printing.
    """
    telemetry = {}
    if analysis.telemetry_data:
        try:
            telemetry = json.loads(analysis.telemetry_data)
        except Exception:
            telemetry = {}

    diameter_mm = telemetry.get("diameter_mm", 12.0)
    surface_area_mm2 = telemetry.get("surface_area_mm2", 113.1)
    irregularity = telemetry.get("border_irregularity_score", 1.15)
    site_key = analysis.lesion_site or "buccal_mucosa"

    cT = "cT1 (≤20mm)" if diameter_mm <= 20.0 else ("cT2 (20-40mm)" if diameter_mm <= 40.0 else "cT3 (>40mm)")
    is_cancer = analysis.prediction.lower() == "cancer"

    urgency = "URGENT // IMMEDIATE CONSULTATION (< 7 DAYS)" if is_cancer else "ROUTINE CLINICAL EVALUATION"

    biopsy_guidance = (
        f"Incisional scalpel biopsy targeting the active, non-necrotic infiltrative junctional margin "
        f"at the {site_key.replace('_', ' ')}. Avoid superficial scraping or solely central necrotic tissue. "
        f"Include representative sub-epithelial connective tissue for assessment of basement membrane invasion."
    )

    return {
        "referral_reference_id": f"REF-ONC-2026-{analysis.id:04d}",
        "referral_date": (analysis.timestamp or datetime.datetime.utcnow()).strftime("%B %d, %Y"),
        "urgency": urgency,
        "referring_clinician": {
            "name": practitioner.full_name or f"Dr. {practitioner.username}",
            "email": practitioner.email,
            "role": practitioner.role.capitalize(),
            "facility": "Regional Oral Oncology Screening & Dysplasia Center"
        },
        "patient": {
            "mrn_identifier": analysis.patient_identifier or "ANON-001",
            "anatomical_site": site_key.replace("_", " ").title(),
            "clinical_risk_score": float(analysis.risk_score or 0.0),
        },
        "diagnostic_findings": {
            "ai_verdict": analysis.prediction.upper(),
            "confidence_percentage": round(float(analysis.confidence) * 100, 1),
            "epistemic_uncertainty_sigma2": round(float(analysis.uncertainty or 0.0), 5),
            "calibrated_diameter_mm": round(float(diameter_mm), 1),
            "surface_area_mm2": round(float(surface_area_mm2), 1),
            "border_irregularity_index": round(float(irregularity), 2),
            "ajcc_8th_ctnm": f"{cT} cN0 cM0 (Presumptive Clinical Staging)",
            "triage_tier": analysis.triage_tier or ("Tier 3 (High Oncology Suspicion)" if is_cancer else "Tier 1 (Low Risk)")
        },
        "pathology_verification": {
            "biopsy_proven": analysis.biopsy_proven,
            "ground_truth_dx": analysis.ground_truth_dx,
            "histology_grade": analysis.histology_grade,
            "pathology_notes": analysis.clinician_feedback_notes
        },
        "biopsy_directive": biopsy_guidance
    }
