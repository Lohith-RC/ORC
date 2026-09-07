import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Analysis(Base):
    __tablename__ = "analyses"
    __table_args__ = (
        Index("idx_analyses_user_timestamp", "user_id", "timestamp"),
        Index("idx_analyses_patient_site", "user_id", "patient_identifier", "lesion_site"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    patient_identifier = Column(String(64), default="ANON-001", index=True, nullable=True) # MRN / Patient Tracking ID
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    uncertainty = Column(Float, nullable=True)           # Epistemic variance (MC Dropout)
    risk_score = Column(Float, nullable=True)            # Clinical risk score
    image_quality_score = Column(Float, nullable=True)   # Laplacian variance
    tta_used = Column(Boolean, default=False)
    lesion_site = Column(String, default="buccal_mucosa", nullable=True) # Anatomical oral cavity site
    triage_tier = Column(String(64), nullable=True)      # AJCC 8th Edition Triage Tier
    telemetry_data = Column(Text, nullable=True)         # JSON-encoded spatial morphology telemetry
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    image_filename = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    owner = relationship("User", back_populates="analyses")

