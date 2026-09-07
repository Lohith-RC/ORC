from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import oauth2_scheme
from app.db.session import get_db
from app.models.user import User
from app.models.audit_log import AuditLog

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None or (user.is_active is not None and not user.is_active):
        raise credentials_exception
    return user

def require_role(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required role: {allowed_roles}"
            )
        return current_user
    return role_checker

def log_audit_action(db: Session, action: str, user_id: Optional[int] = None, ip_address: Optional[str] = None, details: Optional[str] = None):
    try:
        log = AuditLog(action=action, user_id=user_id, ip_address=ip_address, details=details)
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()
