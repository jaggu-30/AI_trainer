from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.schemas.auth import TokenResponse
from app.schemas.user import (
    UserCreate,
    UserProfileUpdate,
    UserResponse,
)
from app.services.auth import (
    authenticate_user,
    create_user,
    get_user_by_email,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """Register a new fitness application user."""

    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    return create_user(
        db,
        user_data,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate a user and return a JWT access token."""

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_profile(
    current_user=Depends(get_current_user),
):
    """Return the currently authenticated user's profile."""

    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
)
def update_current_user_profile(
    profile_data: UserProfileUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save the profile values used for personalized AI features."""

    updates = profile_data.model_dump(
        exclude_unset=True,
    )

    for field, value in updates.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user
