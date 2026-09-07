import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AnalysisBase(BaseModel):
    prediction: str
    confidence: float
    uncertainty: Optional[float] = None
    risk_score: Optional[float] = None
    image_quality_score: Optional[float] = None
    image_filename: str

class AnalysisInfo(AnalysisBase):
    id: int
    timestamp: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class PredictionResponse(AnalysisBase):
    id: int
    timestamp: datetime.datetime
    image_quality_flag: Optional[str] = None
    recommendation: str

    model_config = ConfigDict(from_attributes=True)
