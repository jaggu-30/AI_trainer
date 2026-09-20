from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.diet import (
    DietMealResponse,
    DietPlanRequest,
    DietPlanResponse,
    GroceryItemResponse,
)
from app.schemas.dietician import (
    DieticianCalculationRequest,
    DieticianCalculationResponse,
)
from app.services.ai.dietician.calculation_service import (
    DieticianCalculationService,
)
from app.services.ai.dietician.service import (
    DieticianService,
)


router = APIRouter(
    prefix="/api/v1/dietician",
    tags=["Dietician"],
)


calculation_service = (
    DieticianCalculationService()
)

dietician_service = DieticianService()


@router.get("/health")
def dietician_health():
    return {
        "status": "healthy",
        "service": "dietician",
    }


@router.post(
    "/calculate",
    response_model=DieticianCalculationResponse,
    status_code=status.HTTP_200_OK,
)
def calculate_nutrition_targets(
    request: DieticianCalculationRequest,
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Calculate BMI, BMR, calorie target,
    and macronutrient targets.
    """

    del current_user

    try:
        result = calculation_service.calculate(
            age=request.age,
            sex=request.sex,
            height_cm=request.height_cm,
            weight_kg=request.weight_kg,
            activity_level=request.activity_level,
            goal=request.goal,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail=str(error),
        ) from error

    return DieticianCalculationResponse(
        bmi=result.bmi,
        bmi_category=result.bmi_category,
        bmr=result.bmr,
        activity_multiplier=(
            result.activity_multiplier
        ),
        activity_level=result.activity_level,
        calorie_target=result.calorie_target,
        calorie_adjustment=(
            result.calorie_adjustment
        ),
        protein_g=result.protein_g,
        carbohydrates_g=(
            result.carbohydrates_g
        ),
        fat_g=result.fat_g,
    )


@router.post(
    "/plan",
    response_model=DietPlanResponse,
    status_code=status.HTTP_200_OK,
)
def generate_dietician_plan(
    request: DietPlanRequest,
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate a complete personalized Dietician plan
    using the authenticated user's stored profile.
    """

    if current_user.age is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Age is required to generate "
                "a diet plan."
            ),
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
            activity_level=(
                current_user.activity_level
            ),
            fitness_goal=(
                current_user.fitness_goal
            ),
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
        target_calories=(
            plan.target_calories
        ),
        meals=[
            DietMealResponse(
                name=meal.name,
                calories=meal.calories,
                protein_g=meal.protein_g,
                carbohydrates_g=(
                    meal.carbohydrates_g
                ),
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
