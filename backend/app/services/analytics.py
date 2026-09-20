from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.iot import (
    IoTCommand,
    IoTEquipment,
    IoTTelemetry,
)
from app.models.nutrition import NutritionLog
from app.models.user import User
from app.models.workout import WorkoutSession
from app.schemas.analytics import (
    FitnessAnalyticsResponse,
    NutritionAnalyticsResponse,
    SmartGymAnalyticsResponse,
    WorkoutAnalyticsResponse,
)


class AnalyticsService:
    """Calculate unified fitness analytics for users."""

    def generate(
        self,
        db: Session,
        user: User,
    ) -> FitnessAnalyticsResponse:
        """Generate analytics for one authenticated user."""

        workout_analytics = self._workout_analytics(
            db=db,
            user_id=user.id,
        )

        nutrition_analytics = self._nutrition_analytics(
            db=db,
            user_id=user.id,
        )

        smart_gym_analytics = self._smart_gym_analytics(
            db=db,
        )

        return FitnessAnalyticsResponse(
            generated_at=datetime.utcnow(),
            workouts=workout_analytics,
            nutrition=nutrition_analytics,
            smart_gym=smart_gym_analytics,
        )

    def _workout_analytics(
        self,
        db: Session,
        user_id: int,
    ) -> WorkoutAnalyticsResponse:
        statement = select(
            func.count(WorkoutSession.id),
            func.coalesce(
                func.sum(
                    WorkoutSession.total_repetitions
                ),
                0,
            ),
            func.coalesce(
                func.avg(
                    WorkoutSession.performance_score
                ),
                0.0,
            ),
            func.coalesce(
                func.max(
                    WorkoutSession.performance_score
                ),
                0.0,
            ),
        ).where(
            WorkoutSession.user_id == user_id
        )

        (
            total_workouts,
            total_repetitions,
            average_performance,
            best_performance,
        ) = db.execute(statement).one()

        return WorkoutAnalyticsResponse(
            total_workouts=int(total_workouts),
            total_repetitions=int(total_repetitions),
            average_performance_score=round(
                float(average_performance),
                2,
            ),
            best_performance_score=round(
                float(best_performance),
                2,
            ),
        )

    def _nutrition_analytics(
        self,
        db: Session,
        user_id: int,
    ) -> NutritionAnalyticsResponse:
        statement = select(
            func.count(NutritionLog.id),
            func.coalesce(
                func.sum(
                    NutritionLog.calories
                ),
                0.0,
            ),
            func.coalesce(
                func.sum(
                    NutritionLog.protein_g
                ),
                0.0,
            ),
            func.coalesce(
                func.sum(
                    NutritionLog.carbohydrates_g
                ),
                0.0,
            ),
            func.coalesce(
                func.sum(
                    NutritionLog.fat_g
                ),
                0.0,
            ),
        ).where(
            NutritionLog.user_id == user_id
        )

        (
            total_entries,
            total_calories,
            total_protein,
            total_carbohydrates,
            total_fat,
        ) = db.execute(statement).one()

        return NutritionAnalyticsResponse(
            total_food_entries=int(total_entries),
            total_calories=round(
                float(total_calories),
                2,
            ),
            total_protein_g=round(
                float(total_protein),
                2,
            ),
            total_carbohydrates_g=round(
                float(total_carbohydrates),
                2,
            ),
            total_fat_g=round(
                float(total_fat),
                2,
            ),
        )

    def _smart_gym_analytics(
        self,
        db: Session,
    ) -> SmartGymAnalyticsResponse:
        equipment_count = int(
            db.scalar(
                select(
                    func.count(
                        IoTEquipment.id
                    )
                )
            )
            or 0
        )

        telemetry_statement = select(
            func.count(
                IoTTelemetry.id
            ),
            func.coalesce(
                func.avg(
                    IoTTelemetry.performance_score
                ),
                0.0,
            ),
            func.coalesce(
                func.avg(
                    IoTTelemetry.fatigue_level
                ),
                0.0,
            ),
            func.coalesce(
                func.avg(
                    IoTTelemetry.heart_rate
                ),
                0.0,
            ),
            func.coalesce(
                func.avg(
                    IoTTelemetry.resistance_level
                ),
                0.0,
            ),
        )

        (
            telemetry_samples,
            average_performance,
            average_fatigue,
            average_heart_rate,
            average_resistance,
        ) = db.execute(
            telemetry_statement
        ).one()

        total_commands = int(
            db.scalar(
                select(
                    func.count(
                        IoTCommand.id
                    )
                )
            )
            or 0
        )

        increase_commands = int(
            db.scalar(
                select(
                    func.count(
                        IoTCommand.id
                    )
                ).where(
                    IoTCommand.action
                    == "increase_resistance"
                )
            )
            or 0
        )

        decrease_commands = int(
            db.scalar(
                select(
                    func.count(
                        IoTCommand.id
                    )
                ).where(
                    IoTCommand.action
                    == "decrease_resistance"
                )
            )
            or 0
        )

        return SmartGymAnalyticsResponse(
            equipment_count=equipment_count,
            telemetry_samples=int(
                telemetry_samples
            ),
            average_performance_score=round(
                float(average_performance),
                2,
            ),
            average_fatigue_level=round(
                float(average_fatigue),
                2,
            ),
            average_heart_rate=round(
                float(average_heart_rate),
                2,
            ),
            average_resistance=round(
                float(average_resistance),
                2,
            ),
            total_commands=total_commands,
            increase_commands=increase_commands,
            decrease_commands=decrease_commands,
        )