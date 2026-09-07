import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AnalysisBase(BaseModel):
    prediction: str
    confidence: float
    uncertainty: Optional[float] = None
    risk_score: Optional[float] = None
    image_quality_score: Optional[float] = None
    lesion_site: Optional[str] = "buccal_mucosa"
    patient_identifier: Optional[str] = "ANON-001"
    triage_tier: Optional[str] = None
    telemetry_data: Optional[str] = None
    biopsy_proven: Optional[bool] = False
    ground_truth_dx: Optional[str] = None
    histology_grade: Optional[str] = None
    clinician_feedback_notes: Optional[str] = None
    annotated_contour: Optional[str] = None
    verified_at: Optional[datetime.datetime] = None
    verified_by_user_id: Optional[int] = None
    image_filename: str


class AnalysisInfo(AnalysisBase):
    id: int
    timestamp: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ClinicianVerificationRequest(BaseModel):
    ground_truth_dx: str # e.g. OSCC_MALIGNANT, HIGH_GRADE_DYSPLASIA, MILD_MOD_DYSPLASIA, LICHEN_PLANUS, TRAUMATIC_ULCER, BENIGN_HYPERKERATOSIS, NORMAL_MUCOSA
    biopsy_proven: bool = False
    histology_grade: Optional[str] = "NOT_APPLICABLE" # WELL_DIFFERENTIATED, MODERATELY_DIFFERENTIATED, POORLY_DIFFERENTIATED, NOT_APPLICABLE
    clinician_feedback_notes: Optional[str] = None
    annotated_contour: Optional[str] = None # JSON string of contour coordinates


class ActiveLearningQueueItem(BaseModel):
    analysis_id: int
    patient_identifier: str
    lesion_site: str
    prediction: str
    confidence: float
    uncertainty: float
    risk_score: float
    triage_tier: Optional[str] = None
    timestamp: datetime.datetime
    priority_score: float
    priority_reason: str

    model_config = ConfigDict(from_attributes=True)


class FlywheelMetricsResponse(BaseModel):
    total_screenings: int
    verified_count: int
    biopsy_proven_count: int
    unverified_queue_count: int
    concordance_rate: float
    flywheel_maturation_pct: float
