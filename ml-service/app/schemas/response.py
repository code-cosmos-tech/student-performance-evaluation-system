from typing import Dict
from pydantic import BaseModel, Field, field_validator, ValidationError


class PredictionResponse(BaseModel):
    performance_category: str = Field(description="Student's performance category")
    confidence: float
    probabilities: Dict[str, float]

    @field_validator('performance_category')
    @classmethod
    def validate_performance_category(cls, v: str) -> str:
        valid_performance_categories = ['Average', 'At Risk', 'Good']
        if v not in valid_performance_categories:
            raise ValidationError(f"Performance category must be one of {valid_performance_categories}")
        return v
