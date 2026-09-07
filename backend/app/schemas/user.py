import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "clinician"

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @field_validator("email")
    @classmethod
    def email_basic_check(cls, v: Optional[str]) -> Optional[str]:
        if v and "@" not in v:
            raise ValueError("Invalid email address — must contain '@'")
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
