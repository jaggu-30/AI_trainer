from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage, ChatSession
from app.models.iot import (
    IoTCommand,
    IoTEquipment,
    IoTTelemetry,
)
from app.models.nutrition import NutritionLog
from app.models.user import User
from app.models.workout import WorkoutSession
from app.schemas.admin import (
    AdminChatSummary,
    AdminNutritionSummary,
    AdminSmartGymSummary,
    AdminSummaryResponse,
    AdminUserSummary,
    AdminWorkoutSummary,
)


class AdminService:
    """Generate system-wide administration statistics."""

    def generate_summary(
        self,
        db: Session,
    ) -> AdminSummaryResponse:
        users = self._users(db)
        workouts = self._workouts(db)
        nutrition = self._nutrition(db)
        chat = self._chat(db)
        smart_gym = self._smart_gym(db)

        return AdminSummaryResponse(
            users=users,
            workouts=workouts,
            nutrition=nutrition,
            chat=chat,
            smart_gym=smart_gym,
        )

    def _users(
        self,
        db: Session,
    ) -> AdminUserSummary:
        total_users = int(
            db.scalar(
                select(
                    func.count(User.id)
                )
            )
            or 0
        )

        active_users = int(
            db.scalar(
                select(
                    func.count(User.id)
                ).where(
                    User.is_active.is_(True)
                )
            )
            or 0
        )

        admin_users = int(
            db.scalar(
                select(
                    func.count(User.id)
                ).where(
                    User.is_admin.is_(True)
                )
            )
            or 0
        )

        return AdminUserSummary(
            total_users=total_users,
            active_users=active_users,
            inactive_users=(
                total_users - active_users
            ),
            admin_users=admin_users,
        )

    def _workouts(
        self,
        db: Session,
    ) -> AdminWorkoutSummary:
        (
            total_workouts,
            total_repetitions,
            average_performance,
            best_performance,
        ) = db.execute(
            select(
                func.count(
                    WorkoutSession.id
                ),
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
            )
        ).one()

        return AdminWorkoutSummary(
            total_workouts=int(
                total_workouts
            ),
            total_repetitions=int(
                total_repetitions
            ),
            average_performance_score=round(
                float(
                    average_performance
                ),
                2,
            ),
            best_performance_score=round(
                float(
                    best_performance
                ),
                2,
            ),
        )

    def _nutrition(
        self,
        db: Session,
    ) -> AdminNutritionSummary:
        (
            total_entries,
            total_calories,
            total_protein,
            total_carbohydrates,
            total_fat,
        ) = db.execute(
            select(
                func.count(
                    NutritionLog.id
                ),
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
            )
        ).one()

        return AdminNutritionSummary(
            total_food_entries=int(
                total_entries
            ),
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

    def _chat(
        self,
        db: Session,
    ) -> AdminChatSummary:
        total_sessions = int(
            db.scalar(
                select(
                    func.count(
                        ChatSession.id
                    )
                )
            )
            or 0
        )

        total_messages = int(
            db.scalar(
                select(
                    func.count(
                        ChatMessage.id
                    )
                )
            )
            or 0
        )

        user_messages = int(
            db.scalar(
                select(
                    func.count(
                        ChatMessage.id
                    )
                ).where(
                    ChatMessage.role
                    == "user"
                )
            )
            or 0
        )

        assistant_messages = int(
            db.scalar(
                select(
                    func.count(
                        ChatMessage.id
                    )
                ).where(
                    ChatMessage.role
                    == "assistant"
                )
            )
            or 0
        )

        return AdminChatSummary(
            total_sessions=total_sessions,
            total_messages=total_messages,
            user_messages=user_messages,
            assistant_messages=assistant_messages,
        )

    def _smart_gym(
        self,
        db: Session,
    ) -> AdminSmartGymSummary:
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

        telemetry_samples = int(
            db.scalar(
                select(
                    func.count(
                        IoTTelemetry.id
                    )
                )
            )
            or 0
        )

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

        return AdminSmartGymSummary(
            equipment_count=equipment_count,
            telemetry_samples=telemetry_samples,
            total_commands=total_commands,
            increase_commands=increase_commands,
            decrease_commands=decrease_commands,
        )