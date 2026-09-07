import datetime
from typing import Optional
from pydantic import BaseModel

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

    class Config:
        from_attributes = True

class PredictionResponse(AnalysisBase):
    id: int
    timestamp: datetime.datetime
    image_quality_flag: Optional[str] = None
    recommendation: str

    class Config:
        from_attributes = True
