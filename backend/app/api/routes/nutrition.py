from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.nutrition import NutritionLog
from app.models.user import User
from app.schemas.nutrition import (
    NutritionLogCreate,
    NutritionLogResponse,
    NutritionSummaryResponse,
)


router = APIRouter(
    prefix="/api/v1/nutrition",
    tags=["Nutrition"],
)


@router.post(
    "",
    response_model=NutritionLogResponse,
    status_code=201,
)
def create_nutrition_log(
    nutrition_data: NutritionLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create one nutrition-intake entry for the
    authenticated user.
    """

    consumed_at = nutrition_data.consumed_at

    if consumed_at is None:
        consumed_at = datetime.now(timezone.utc).replace(
            tzinfo=None
        )

    nutrition_log = NutritionLog(
        user_id=current_user.id,
        food_name=nutrition_data.food_name.strip(),
        quantity=nutrition_data.quantity,
        calories=nutrition_data.calories,
        protein_g=nutrition_data.protein_g,
        carbohydrates_g=nutrition_data.carbohydrates_g,
        fat_g=nutrition_data.fat_g,
        consumed_at=consumed_at,
    )

    db.add(nutrition_log)
    db.commit()
    db.refresh(nutrition_log)

    return nutrition_log


@router.get(
    "",
    response_model=list[NutritionLogResponse],
)
def get_nutrition_history(
    food_name: str | None = Query(
        default=None,
        min_length=1,
        max_length=150,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return nutrition-intake history for the
    authenticated user.
    """

    filters = [
        NutritionLog.user_id == current_user.id
    ]

    if food_name is not None:
        filters.append(
            NutritionLog.food_name.ilike(
                f"%{food_name.strip()}%"
            )
        )

    statement = (
        select(NutritionLog)
        .where(*filters)
        .order_by(
            NutritionLog.consumed_at.desc(),
            NutritionLog.id.desc(),
        )
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/summary",
    response_model=NutritionSummaryResponse,
)
def get_nutrition_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return aggregate nutrition intake for the
    authenticated user.
    """

    statement = select(
        func.count(NutritionLog.id),
        func.coalesce(
            func.sum(NutritionLog.calories),
            0.0,
        ),
        func.coalesce(
            func.sum(NutritionLog.protein_g),
            0.0,
        ),
        func.coalesce(
            func.sum(
                NutritionLog.carbohydrates_g
            ),
            0.0,
        ),
        func.coalesce(
            func.sum(NutritionLog.fat_g),
            0.0,
        ),
    ).where(
        NutritionLog.user_id == current_user.id
    )

    result = db.execute(statement).one()

    (
        total_entries,
        total_calories,
        total_protein_g,
        total_carbohydrates_g,
        total_fat_g,
    ) = result

    return NutritionSummaryResponse(
        total_entries=int(total_entries),
        total_calories=round(
            float(total_calories),
            2,
        ),
        total_protein_g=round(
            float(total_protein_g),
            2,
        ),
        total_carbohydrates_g=round(
            float(total_carbohydrates_g),
            2,
        ),
        total_fat_g=round(
            float(total_fat_g),
            2,
        ),
    )
