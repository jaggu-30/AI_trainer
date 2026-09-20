from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.db.database import get_db
from app.models.user import User
from app.schemas.admin import (
    AdminSummaryResponse,
    AdminUserListResponse,
    AdminUserResponse,
    AdminUserStatusUpdate,
)
from app.services.admin import AdminService


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
)


admin_service = AdminService()


@router.get(
    "/summary",
    response_model=AdminSummaryResponse,
)
def get_admin_summary(
    current_user: User = Depends(
        require_admin
    ),
    db: Session = Depends(get_db),
):
    """
    Return system-wide statistics for administrators.
    """

    del current_user

    return admin_service.generate_summary(
        db=db,
    )


@router.get(
    "/users",
    response_model=AdminUserListResponse,
)
def list_users(
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Return the user directory to an authenticated administrator."""

    del current_user

    total = db.scalar(
        select(func.count(User.id))
    ) or 0

    users = list(
        db.scalars(
            select(User)
            .order_by(User.created_at.desc(), User.id.desc())
            .offset(offset)
            .limit(limit)
        ).all()
    )

    return AdminUserListResponse(
        items=[
            AdminUserResponse.model_validate(user)
            for user in users
        ],
        total=int(total),
        limit=limit,
        offset=offset,
    )


@router.patch(
    "/users/{user_id}/status",
    response_model=AdminUserResponse,
)
def update_user_status(
    user_id: int,
    payload: AdminUserStatusUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Allow an admin to activate or deactivate another user account."""

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if user.id == current_user.id and not payload.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Administrators cannot deactivate their own account.",
        )

    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)

    return user
