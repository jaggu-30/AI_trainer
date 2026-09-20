from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.diet import (
    DietMealResponse,
    DietPlanRequest,
    DietPlanResponse,
    GroceryItemResponse,
)
from app.services.ai.dietician.service import DieticianService


router = APIRouter(
    prefix="/api/v1/diet",
    tags=["Diet"],
)


dietician_service = DieticianService()


@router.post(
    "/plan",
    response_model=DietPlanResponse,
)
def generate_diet_plan(
    request: DietPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a personalized diet plan using the
    authenticated user's stored profile.
    """

    del db

    if current_user.age is None:
        raise HTTPException(
            status_code=400,
            detail="Age is required to generate a diet plan.",
        )

    if current_user.height_cm is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Height is required to generate "
                "a diet plan."
            ),
        )

    if current_user.weight_kg is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Weight is required to generate "
                "a diet plan."
            ),
        )

    if not current_user.sex:
        raise HTTPException(
            status_code=400,
            detail=(
                "Complete your fitness profile before generating "
                "a diet plan."
            ),
        )

    if current_user.activity_level is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Activity level is required to generate "
                "a diet plan."
            ),
        )

    if current_user.fitness_goal is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Fitness goal is required to generate "
                "a diet plan."
            ),
        )

    dietary_preference = (
        current_user.dietary_preference
        or "balanced"
    )

    try:
        plan = dietician_service.generate_plan(
            age=current_user.age,
            weight_kg=current_user.weight_kg,
            height_cm=current_user.height_cm,
            sex=current_user.sex,
            activity_level=current_user.activity_level,
            fitness_goal=current_user.fitness_goal,
            dietary_preference=dietary_preference,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return DietPlanResponse(
        bmi=plan.bmi,
        bmi_category=plan.bmi_category,
        bmr=plan.bmr,
        maintenance_calories=(
            plan.maintenance_calories
        ),
        target_calories=plan.target_calories,
        meals=[
            DietMealResponse(
                name=meal.name,
                calories=meal.calories,
                protein_g=meal.protein_g,
                carbohydrates_g=meal.carbohydrates_g,
                fat_g=meal.fat_g,
            )
            for meal in plan.meal_plan.meals
        ],
        grocery_list=[
            GroceryItemResponse(
                name=item.name,
                quantity=item.quantity,
                unit=item.unit,
                category=item.category,
            )
            for item in plan.grocery_items
        ],
    )
