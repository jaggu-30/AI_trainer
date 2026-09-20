from sqlalchemy import func
from sqlalchemy.orm import Session

from ai.dietician.context import DietConversationContext, DietContextBuilder
from ai.dietician.conversation import DietConversationEngine
from ai.dietician.llm import DietLLMService

from app.core.config import settings
from app.models.nutrition import NutritionLog
from app.models.user import User
from app.services.ai.dietician.service import DieticianService


class DieticianChatService:
    def __init__(self) -> None:
        self.dietician = DieticianService()
        self.context_builder = DietContextBuilder()
        self.conversation_engine = DietConversationEngine()

    def _validate_profile(self, user: User) -> None:
        required_fields = {
            "age": user.age,
            "height_cm": user.height_cm,
            "weight_kg": user.weight_kg,
            "activity_level": user.activity_level,
            "fitness_goal": user.fitness_goal,
        }

        missing = [
            field
            for field, value in required_fields.items()
            if value is None
        ]

        if missing:
            raise ValueError(
                "Complete your profile before using the Dietician chatbot. "
                f"Missing fields: {', '.join(missing)}"
            )

    def _get_nutrition_summary(
        self,
        db: Session,
        user: User,
    ) -> dict[str, float]:
        result = (
            db.query(
                func.coalesce(func.sum(NutritionLog.calories), 0.0),
                func.coalesce(func.sum(NutritionLog.protein_g), 0.0),
                func.coalesce(func.sum(NutritionLog.carbohydrates_g), 0.0),
                func.coalesce(func.sum(NutritionLog.fat_g), 0.0),
            )
            .filter(NutritionLog.user_id == user.id)
            .one()
        )

        return {
            "calories": float(result[0]),
            "protein_g": float(result[1]),
            "carbohydrates_g": float(result[2]),
            "fat_g": float(result[3]),
        }

    def _build_system_prompt(
        self,
        user: User,
        context: DietConversationContext,
    ) -> str:
        diet_plan = context.diet_plan
        nutrition = context.nutrition_summary

        return f"""
You are an AI Dietician inside an AI Gym & Fitness Assistant.

User profile:
- Name: {user.full_name}
- Age: {user.age}
- Height: {user.height_cm} cm
- Weight: {user.weight_kg} kg
- Fitness goal: {user.fitness_goal}
- Dietary preference: {user.dietary_preference or "balanced"}
- Activity level: {user.activity_level}

Calculated diet information:
- BMI: {diet_plan.bmi:.2f}
- BMI category: {diet_plan.bmi_category}
- BMR: {diet_plan.bmr:.2f} kcal/day
- Maintenance calories: {diet_plan.maintenance_calories:.2f} kcal/day
- Target calories: {diet_plan.target_calories:.2f} kcal/day

Recorded nutrition intake:
- Calories: {nutrition["calories"]:.2f} kcal
- Protein: {nutrition["protein_g"]:.2f} g
- Carbohydrates: {nutrition["carbohydrates_g"]:.2f} g
- Fat: {nutrition["fat_g"]:.2f} g

Provide concise, practical fitness and nutrition guidance.
Use the user's profile and recorded data when relevant.
Do not invent measurements or nutrition records.
""".strip()

    def respond(
        self,
        db: Session,
        user: User,
        user_message: str,
        sex: str,
    ) -> tuple[str, str]:
        self._validate_profile(user)

        nutrition_summary = self._get_nutrition_summary(
            db=db,
            user=user,
        )

        diet_data = self.dietician.generate_plan(
            sex=sex,
            age=user.age,
            height_cm=user.height_cm,
            weight_kg=user.weight_kg,
            activity_level=user.activity_level,
            fitness_goal=user.fitness_goal,
            dietary_preference=user.dietary_preference or "balanced",
        )

        context = self.context_builder.build(
            diet_plan=diet_data,
            nutrition_summary=nutrition_summary,
        )

        intent = self.conversation_engine.intent_detector.detect(
            user_message
        )

        system_prompt = self._build_system_prompt(
            user=user,
            context=context,
        )

        llm_service = DietLLMService(
            conversation_engine=self.conversation_engine,
            context=context,
            api_key=settings.openai_api_key,
        )

        provider = llm_service.create_provider()

        response = provider.generate(
            system_prompt=system_prompt,
            user_message=user_message,
        )

        return response, intent.value