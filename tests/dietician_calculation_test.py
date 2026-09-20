import pytest

from app.services.ai.dietician.calculation_service import (
    DieticianCalculationService,
)


def create_service() -> DieticianCalculationService:
    return DieticianCalculationService()


def test_weight_loss_calculation():
    service = create_service()

    result = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        goal="weight_loss",
    )

    assert result.bmi == 22.86
    assert result.bmi_category == "normal"

    assert result.bmr == 1673.75
    assert result.activity_multiplier == 1.55

    assert result.calorie_target == 2094.31
    assert result.calorie_adjustment == -500.0

    assert result.protein_g == 112.0
    assert result.fat_g == 58.18
    assert result.carbohydrates_g == 280.67


def test_maintenance_calculation():
    service = create_service()

    result = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        goal="maintenance",
    )

    assert result.bmi == 22.86
    assert result.bmi_category == "normal"

    assert result.bmr == 1673.75
    assert result.activity_multiplier == 1.55

    assert result.calorie_target == 2594.31
    assert result.calorie_adjustment == 0.0


def test_weight_gain_calculation():
    service = create_service()

    result = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        goal="weight_gain",
    )

    assert result.calorie_target == 2894.31
    assert result.calorie_adjustment == 300.0


def test_strength_goal_matches_muscle_gain():
    service = create_service()

    strength = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        goal="strength",
    )

    muscle_gain = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        goal="muscle_gain",
    )

    assert (
        strength.calorie_target
        == muscle_gain.calorie_target
    )

    assert (
        strength.calorie_adjustment
        == muscle_gain.calorie_adjustment
    )


def test_case_insensitive_inputs():
    service = create_service()

    result = service.calculate(
        age=25,
        sex="MALE",
        height_cm=175,
        weight_kg=70,
        activity_level="MODERATE",
        goal="MAINTENANCE",
    )

    assert result.bmi == 22.86
    assert result.bmi_category == "normal"
    assert result.calorie_target == 2594.31


def test_invalid_sex():
    service = create_service()

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="other",
            height_cm=175,
            weight_kg=70,
            activity_level="moderate",
            goal="maintenance",
        )


def test_invalid_activity_level():
    service = create_service()

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="male",
            height_cm=175,
            weight_kg=70,
            activity_level="unknown",
            goal="maintenance",
        )


def test_invalid_goal():
    service = create_service()

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="male",
            height_cm=175,
            weight_kg=70,
            activity_level="moderate",
            goal="unknown",
        )


def test_invalid_age():
    service = create_service()

    with pytest.raises(ValueError):
        service.calculate(
            age=12,
            sex="male",
            height_cm=175,
            weight_kg=70,
            activity_level="moderate",
            goal="maintenance",
        )


def test_invalid_height():
    service = create_service()

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="male",
            height_cm=99,
            weight_kg=70,
            activity_level="moderate",
            goal="maintenance",
        )


def test_invalid_weight():
    service = create_service()

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="male",
            height_cm=175,
            weight_kg=24,
            activity_level="moderate",
            goal="maintenance",
        )


def test_deterministic_result():
    service = create_service()

    first = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        goal="weight_loss",
    )

    second = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        goal="weight_loss",
    )

    assert first == second