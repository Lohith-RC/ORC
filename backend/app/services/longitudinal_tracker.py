import json
import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.models.analysis import Analysis

class TrajectoryStatus(str, Enum):
    BASELINE_INITIAL = "BASELINE_INITIAL"
    STABLE_PERSISTENCE = "STABLE_PERSISTENCE"
    INDOLENT_EXPANSION = "INDOLENT_EXPANSION"
    RAPID_EXPANSION_CRITICAL = "RAPID_EXPANSION_CRITICAL"
    REGRESSION_RESOLVING = "REGRESSION_RESOLVING"

class LongitudinalDelta(BaseModel):
    has_prior: bool = False
    prior_analysis_id: Optional[int] = None
    prior_timestamp: Optional[str] = None
    elapsed_days: float = 0.0
    prior_diameter_mm: Optional[float] = None
    current_diameter_mm: float
    delta_diameter_mm: Optional[float] = None
    prior_surface_area_mm2: Optional[float] = None
    current_surface_area_mm2: float
    delta_surface_area_mm2: Optional[float] = None
    percentage_change_area: Optional[float] = None
    growth_velocity_mm2_per_day: Optional[float] = None
    prior_border_irregularity: Optional[float] = None
    current_border_irregularity: float
    delta_irregularity: Optional[float] = None
    prior_contour_points: Optional[List[Tuple[float, float]]] = None
    current_contour_points: List[Tuple[float, float]] = Field(default_factory=list)
    trajectory_status: TrajectoryStatus
    trajectory_status_display: str
    clinical_directive: str

def compute_longitudinal_delta(
    current_area_mm2: float,
    current_diameter_mm: float,
    current_irregularity: float,
    current_contour: List[Tuple[float, float]],
    current_timestamp: datetime.datetime,
    prior_analysis: Optional[Analysis] = None
) -> LongitudinalDelta:
    """
    Computes growth velocity (delta area / day), geometric progression, and trajectory classification.
    Flags progressive epithelial dysplasia or rapidly growing squamous cell carcinoma.
    """
    if prior_analysis is None:
        return LongitudinalDelta(
            has_prior=False,
            current_diameter_mm=round(current_diameter_mm, 1),
            current_surface_area_mm2=round(current_area_mm2, 1),
            current_border_irregularity=round(current_irregularity, 2),
            current_contour_points=current_contour,
            trajectory_status=TrajectoryStatus.BASELINE_INITIAL,
            trajectory_status_display="Baseline Index Encounter",
            clinical_directive=(
                "First documented digital optical record for this anatomical lesion site. "
                "Baseline geometry and margin coordinates stored for longitudinal surveillance."
            )
        )

    # Parse prior telemetry JSON if available
    prior_telem = {}
    if prior_analysis.telemetry_data:
        try:
            prior_telem = json.loads(prior_analysis.telemetry_data)
        except Exception:
            prior_telem = {}

    prior_area = float(prior_telem.get("surface_area_mm2", 0.0))
    prior_diam = float(prior_telem.get("diameter_mm", 0.0))
    prior_irreg = float(prior_telem.get("border_irregularity_score", 1.0))
    prior_contour = prior_telem.get("contour_points", [])

    # If prior telemetry was unpopulated, derive from conservative fallback
    if prior_area <= 0.0:
        prior_area = 113.1 # ~12mm circular baseline
    if prior_diam <= 0.0:
        prior_diam = 12.0

    # Elapsed interval calculation (minimum 0.1 days to avoid division by zero)
    prior_time = prior_analysis.timestamp or (current_timestamp - datetime.timedelta(days=14))
    elapsed_seconds = max(3600.0, (current_timestamp - prior_time).total_seconds())
    elapsed_days = round(elapsed_seconds / 86400.0, 1)

    delta_area = round(current_area_mm2 - prior_area, 2)
    delta_diam = round(current_diameter_mm - prior_diam, 1)
    delta_irreg = round(current_irregularity - prior_irreg, 2)
    
    pct_change = round((delta_area / max(1.0, prior_area)) * 100.0, 1)
    velocity_per_day = round(delta_area / max(0.5, elapsed_days), 3)

    # Trajectory Decision Matrix
    # Rapid expansion: >15% expansion or velocity > 0.40 mm2/day or diameter expansion > 3mm
    if pct_change >= 15.0 or velocity_per_day >= 0.40 or delta_diam >= 3.0:
        status = TrajectoryStatus.RAPID_EXPANSION_CRITICAL
        display = "CRITICAL // Rapid Mucosal Lesion Expansion"
        directive = (
            f"Lesion area has expanded by {pct_change}% (+{delta_area} mm²) at a velocity of {velocity_per_day} mm²/day over {elapsed_days} days. "
            "Rapid dimensional expansion strongly signals active malignant transformation. "
            "Immediate surgical biopsy escalation is mandatory."
        )
    # Regression: >10% area decrease
    elif pct_change <= -10.0 or delta_diam <= -2.0:
        status = TrajectoryStatus.REGRESSION_RESOLVING
        display = "POSITIVE // Lesion Regression Observed"
        directive = (
            f"Lesion has contracted by {abs(pct_change)}% (-{abs(delta_area)} mm²) over {elapsed_days} days. "
            "Suggestive of resolving inflammatory response or healing post-irritant removal. "
            "Continue conservative observation until complete epithelial clearance."
        )
    # Indolent expansion: 5% to 15%
    elif pct_change >= 5.0:
        status = TrajectoryStatus.INDOLENT_EXPANSION
        display = "ELEVATED // Indolent Low-Grade Expansion"
        directive = (
            f"Mild area increase of {pct_change}% (+{delta_area} mm²) observed over {elapsed_days} days. "
            "Progressive non-healing lesion warrants 7-day follow-up or incisional diagnostic sampling."
        )
    # Stable persistence: within +/- 5%
    else:
        status = TrajectoryStatus.STABLE_PERSISTENCE
        display = "STABLE // Static Mucosal Architecture"
        directive = (
            f"Lesion dimensions are unchanged ({pct_change}%, {delta_area} mm² delta) over {elapsed_days} days. "
            "Persistent static leukoplakia/erythroplakia requires continued histological vigilance."
        )

    return LongitudinalDelta(
        has_prior=True,
        prior_analysis_id=prior_analysis.id,
        prior_timestamp=prior_time.strftime("%Y-%m-%d %H:%M"),
        elapsed_days=elapsed_days,
        prior_diameter_mm=round(prior_diam, 1),
        current_diameter_mm=round(current_diameter_mm, 1),
        delta_diameter_mm=delta_diam,
        prior_surface_area_mm2=round(prior_area, 1),
        current_surface_area_mm2=round(current_area_mm2, 1),
        delta_surface_area_mm2=delta_area,
        percentage_change_area=pct_change,
        growth_velocity_mm2_per_day=velocity_per_day,
        prior_border_irregularity=round(prior_irreg, 2),
        current_border_irregularity=round(current_irregularity, 2),
        delta_irregularity=delta_irreg,
        prior_contour_points=prior_contour,
        current_contour_points=current_contour,
        trajectory_status=status,
        trajectory_status_display=display,
        clinical_directive=directive
    )

def fetch_patient_serial_trajectory(
    db: Session,
    user_id: int,
    patient_identifier: str,
    lesion_site: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Retrieves all historical encounters for a patient and computes serial deltas along the timeline.
    """
    query = db.query(Analysis).filter(
        Analysis.user_id == user_id,
        Analysis.patient_identifier == patient_identifier
    )
    if lesion_site:
        query = query.filter(Analysis.lesion_site == lesion_site)
        
    records = query.order_by(Analysis.timestamp.asc()).all()
    if not records:
        return []

    timeline = []
    for i, record in enumerate(records):
        prior = records[i - 1] if i > 0 else None
        
        # Parse current telemetry
        telem = {}
        if record.telemetry_data:
            try:
                telem = json.loads(record.telemetry_data)
            except Exception:
                telem = {}
                
        area = float(telem.get("surface_area_mm2", 113.1))
        diam = float(telem.get("diameter_mm", 12.0))
        irreg = float(telem.get("border_irregularity_score", 1.15))
        contour = telem.get("contour_points", [])

        delta = compute_longitudinal_delta(
            current_area_mm2=area,
            current_diameter_mm=diam,
            current_irregularity=irreg,
            current_contour=contour,
            current_timestamp=record.timestamp,
            prior_analysis=prior
        )

        timeline.append({
            "analysis_id": record.id,
            "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M"),
            "prediction": record.prediction,
            "confidence": round(record.confidence, 4),
            "uncertainty": record.uncertainty,
            "lesion_site": record.lesion_site,
            "triage_tier": record.triage_tier,
            "delta": delta.dict(),
            "telemetry": telem
        })

    return timeline
