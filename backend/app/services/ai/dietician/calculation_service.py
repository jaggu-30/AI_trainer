from dataclasses import dataclass

from ai.dietician.bmi import BMICalculator
from ai.dietician.calorie import CalorieCalculator


@dataclass(frozen=True)
class DieticianCalculationResult:
    """
    Combined BMI, calorie, and macronutrient calculation
    result used by the backend Dietician services.
    """

    bmi: float
    bmi_category: str

    bmr: float
    maintenance_calories: float

    activity_multiplier: float
    activity_level: str

    calorie_target: float
    calorie_adjustment: float

    protein_g: float
    carbohydrates_g: float
    fat_g: float


class DieticianCalculationService:
    """
    Central calculation service for the Dietician module.

    BMI and calorie calculations are delegated to the
    already-tested AI Dietician implementations.

    Macronutrient targets are calculated from the resulting
    calorie target.
    """

    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.20,
        "light": 1.375,
        "lightly_active": 1.375,
        "moderate": 1.55,
        "moderately_active": 1.55,
        "active": 1.725,
        "very_active": 1.725,
        "extra_active": 1.90,
    }

    def __init__(self) -> None:
        self.bmi_calculator = BMICalculator()
        self.calorie_calculator = CalorieCalculator()

    def calculate(
        self,
        age: int,
        sex: str,
        height_cm: float,
        weight_kg: float,
        activity_level: str,
        goal: str,
    ) -> DieticianCalculationResult:
        """
        Calculate BMI, calorie requirements, and
        macronutrient targets.
        """

        normalized_sex = sex.strip().lower()
        normalized_activity = (
            activity_level.strip().lower()
        )
        normalized_goal = goal.strip().lower()

        if age < 13 or age > 100:
            raise ValueError(
                "Age must be between 13 and 100."
            )

        if height_cm < 100 or height_cm > 250:
            raise ValueError(
                "Height must be between 100 and 250 cm."
            )

        if weight_kg < 25 or weight_kg > 300:
            raise ValueError(
                "Weight must be between 25 and 300 kg."
            )

        bmi_result = self.bmi_calculator.calculate(
            weight_kg=weight_kg,
            height_cm=height_cm,
        )

        calorie_result = self.calorie_calculator.calculate(
            age=age,
            weight_kg=weight_kg,
            height_cm=height_cm,
            sex=normalized_sex,
            activity_level=normalized_activity,
            fitness_goal=normalized_goal,
        )

        activity_multiplier = (
            self.ACTIVITY_MULTIPLIERS.get(
                normalized_activity
            )
        )

        if activity_multiplier is None:
            raise ValueError(
                f"Unsupported activity level: "
                f"{activity_level}"
            )

        calorie_adjustment = round(
            calorie_result.target_calories
            - calorie_result.maintenance_calories,
            2,
        )

        protein_g = round(
            weight_kg * 1.6,
            2,
        )

        fat_g = round(
            (
                calorie_result.target_calories
                * 0.25
            )
            / 9,
            2,
        )

        protein_calories = protein_g * 4
        fat_calories = fat_g * 9

        remaining_calories = max(
            calorie_result.target_calories
            - protein_calories
            - fat_calories,
            0.0,
        )

        carbohydrates_g = round(
            remaining_calories / 4,
            2,
        )

        return DieticianCalculationResult(
            bmi=bmi_result.bmi,
            bmi_category=bmi_result.category,
            bmr=calorie_result.bmr,
            maintenance_calories=(
                calorie_result.maintenance_calories
            ),
            activity_multiplier=activity_multiplier,
            activity_level=normalized_activity,
            calorie_target=calorie_result.target_calories,
            calorie_adjustment=calorie_adjustment,
            protein_g=protein_g,
            carbohydrates_g=carbohydrates_g,
            fat_g=fat_g,
        )