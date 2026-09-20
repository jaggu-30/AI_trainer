from pydantic import BaseModel, Field


class DietPlanRequest(BaseModel):
    """Request a plan using the authenticated user's saved profile."""

    # The request is intentionally empty. Profile details are kept in the
    # account so the user never needs to re-enter them on this screen.
    pass


class DietMealResponse(BaseModel):
    """Return one meal in a diet plan."""

    name: str
    calories: float = Field(
        ge=0,
    )
    protein_g: float = Field(
        ge=0,
    )
    carbohydrates_g: float = Field(
        ge=0,
    )
    fat_g: float = Field(
        ge=0,
    )


class GroceryItemResponse(BaseModel):
    """Return one item in the generated grocery list."""

    name: str
    quantity: float = Field(
        gt=0,
    )
    unit: str
    category: str


class DietPlanResponse(BaseModel):
    """Return the complete generated diet plan."""

    bmi: float = Field(
        gt=0,
    )
    bmi_category: str
    bmr: float = Field(
        gt=0,
    )
    maintenance_calories: float = Field(
        gt=0,
    )
    target_calories: float = Field(
        gt=0,
    )
    meals: list[DietMealResponse]
    grocery_list: list[GroceryItemResponse]
