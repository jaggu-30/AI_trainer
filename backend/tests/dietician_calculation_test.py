import pytest

from app.services.ai.dietician.calculation_service import (
    DieticianCalculationService,
)


def test_weight_loss_calculation():
    service = (
        DieticianCalculationService()
    )

    result = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=80,
        activity_level="moderately_active",
        goal="weight_loss",
    )

    assert result.bmi > 0
    assert result.bmi_category == "overweight"

    assert result.bmr > 0

    assert (
        result.activity_multiplier
        == 1.55
    )

    assert (
        result.calorie_adjustment
        == -500.0
    )

    assert (
        result.calorie_target
        > 1200
    )

    assert result.protein_g > 0
    assert result.carbohydrates_g > 0
    assert result.fat_g > 0


def test_maintenance_calculation():
    service = (
        DieticianCalculationService()
    )

    result = service.calculate(
        age=30,
        sex="female",
        height_cm=165,
        weight_kg=65,
        activity_level="lightly_active",
        goal="maintenance",
    )

    assert (
        result.activity_level
        == "lightly_active"
    )

    assert (
        result.calorie_adjustment
        == 0.0
    )

    assert result.calorie_target > 0


def test_weight_gain_calculation():
    service = (
        DieticianCalculationService()
    )

    result = service.calculate(
        age=28,
        sex="male",
        height_cm=180,
        weight_kg=65,
        activity_level="very_active",
        goal="weight_gain",
    )

    assert (
        result.calorie_adjustment
        == 300.0
    )

    assert (
        result.calorie_target > 0
    )


def test_invalid_activity_level():
    service = (
        DieticianCalculationService()
    )

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="male",
            height_cm=175,
            weight_kg=80,
            activity_level="unknown",
            goal="maintenance",
        )


def test_invalid_goal():
    service = (
        DieticianCalculationService()
    )

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="male",
            height_cm=175,
            weight_kg=80,
            activity_level="sedentary",
            goal="unknown",
        )


def test_invalid_sex():
    service = (
        DieticianCalculationService()
    )

    with pytest.raises(ValueError):
        service.calculate(
            age=25,
            sex="unknown",
            height_cm=175,
            weight_kg=80,
            activity_level="sedentary",
            goal="maintenance",
        )


def test_deterministic_result():
    service = (
        DieticianCalculationService()
    )

    first = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=80,
        activity_level="moderately_active",
        goal="maintenance",
    )

    second = service.calculate(
        age=25,
        sex="male",
        height_cm=175,
        weight_kg=80,
        activity_level="moderately_active",
        goal="maintenance",
    )

    assert first == second

    print(
        "BMI:",
        first.bmi,
    )

    print(
        "BMI category:",
        first.bmi_category,
    )

    print(
        "BMR:",
        first.bmr,
    )

    print(
        "Calorie target:",
        first.calorie_target,
    )

    print(
        "Protein:",
        first.protein_g,
    )

    print(
        "Carbohydrates:",
        first.carbohydrates_g,
    )

    print(
        "Fat:",
        first.fat_g,
    )

    print(
        "Dietician calculation tests "
        "passed successfully."
    )