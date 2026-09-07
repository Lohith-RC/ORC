import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.session import Base

class Analysis(Base):
    __tablename__ = "analyses"
    __table_args__ = (
        Index("idx_analyses_user_timestamp", "user_id", "timestamp"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    uncertainty = Column(Float, nullable=True)           # Epistemic variance (MC Dropout)
    risk_score = Column(Float, nullable=True)            # Clinical risk score
    image_quality_score = Column(Float, nullable=True)   # Laplacian variance
    tta_used = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    image_filename = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    owner = relationship("User", back_populates="analyses")
