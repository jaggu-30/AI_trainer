from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class NutritionLog(Base):
    """
    Stores one food-intake entry for an authenticated user.
    """

    __tablename__ = "nutrition_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    food_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    calories: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    protein_g: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    carbohydrates_g: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    fat_g: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    consumed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
