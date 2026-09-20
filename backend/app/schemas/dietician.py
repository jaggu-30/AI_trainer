from pydantic import BaseModel, Field


class DieticianCalculationRequest(BaseModel):
    """
    User profile required for deterministic
    nutrition calculations.
    """

    age: int = Field(
        ge=13,
        le=100,
    )

    sex: str = Field(
        min_length=1,
        max_length=20,
    )

    height_cm: float = Field(
        ge=100,
        le=250,
    )

    weight_kg: float = Field(
        ge=25,
        le=300,
    )

    activity_level: str = Field(
        min_length=1,
        max_length=50,
    )

    goal: str = Field(
        min_length=1,
        max_length=50,
    )


class DieticianCalculationResponse(BaseModel):
    """
    Deterministic nutrition targets returned
    by the Dietician calculation service.
    """

    bmi: float = Field(
        ge=0,
    )

    bmi_category: str

    bmr: float = Field(
        ge=0,
    )

    activity_multiplier: float = Field(
        ge=1.0,
    )

    activity_level: str

    calorie_target: float = Field(
        ge=0,
    )

    calorie_adjustment: float

    protein_g: float = Field(
        ge=0,
    )

    carbohydrates_g: float = Field(
        ge=0,
    )

    fat_g: float = Field(
        ge=0,
    )