from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.analytics import FitnessAnalyticsResponse
from app.services.analytics import AnalyticsService


router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)

analytics_service = AnalyticsService()


@router.get(
    "/summary",
    response_model=FitnessAnalyticsResponse,
)
def get_analytics_summary(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """Return unified fitness analytics."""

    return analytics_service.generate(
        db=db,
        user=current_user,
    )