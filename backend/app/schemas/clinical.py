from pydantic import BaseModel, field_validator

class ClinicalRiskForm(BaseModel):
    """Structured clinical risk factors for multimodal fusion and triage."""
    age: int = 30
    tobacco_use: bool = False
    alcohol_use: bool = False
    betel_nut: bool = False
    prior_lesions: bool = False

    @field_validator("age")
    @classmethod
    def age_range(cls, v: int) -> int:
        if not (5 <= v <= 110):
            raise ValueError("Age must be between 5 and 110")
        return v
