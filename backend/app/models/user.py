import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'clinician', 'patient')", name="chk_valid_user_role"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    role = Column(String, default="clinician", nullable=False)  # admin, clinician, patient
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Immutable historical records: never cascade delete patient records or HIPAA audit logs
    analyses = relationship("Analysis", back_populates="owner", foreign_keys="Analysis.user_id")
    audit_logs = relationship("AuditLog", back_populates="user")
