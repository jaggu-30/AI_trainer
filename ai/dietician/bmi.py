from dataclasses import dataclass


@dataclass(frozen=True)
class BMIResult:
    """Calculated body-mass index result."""

    bmi: float
    category: str


class BMICalculator:
    """Calculate BMI from height and weight."""

    def calculate(
        self,
        weight_kg: float,
        height_cm: float,
    ) -> BMIResult:
        """
        Calculate BMI using:

            BMI = weight_kg / (height_m * height_m)
        """

        if weight_kg <= 0:
            raise ValueError(
                "Weight must be greater than zero."
            )

        if height_cm <= 0:
            raise ValueError(
                "Height must be greater than zero."
            )

        height_m = height_cm / 100.0

        bmi = weight_kg / (height_m * height_m)

        return BMIResult(
            bmi=round(bmi, 2),
            category=self._get_category(bmi),
        )

    @staticmethod
    def _get_category(bmi: float) -> str:
        if bmi < 18.5:
            return "underweight"

        if bmi < 25:
            return "normal"

        if bmi < 30:
            return "overweight"

        return "obesity"
