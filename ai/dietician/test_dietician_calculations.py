from ai.dietician.bmi import BMICalculator
from ai.dietician.calorie import CalorieCalculator


def test_bmi():
    calculator = BMICalculator()

    result = calculator.calculate(
        weight_kg=70,
        height_cm=175,
    )

    assert result.bmi == 22.86
    assert result.category == "normal"

    print(
        f"BMI test: PASSED "
        f"({result.bmi}, {result.category})"
    )


def test_bmi_invalid_weight():
    calculator = BMICalculator()

    try:
        calculator.calculate(
            weight_kg=0,
            height_cm=175,
        )
    except ValueError:
        print("BMI invalid-weight test: PASSED")
        return

    raise AssertionError(
        "BMI calculator accepted zero weight."
    )


def test_bmi_invalid_height():
    calculator = BMICalculator()

    try:
        calculator.calculate(
            weight_kg=70,
            height_cm=0,
        )
    except ValueError:
        print("BMI invalid-height test: PASSED")
        return

    raise AssertionError(
        "BMI calculator accepted zero height."
    )


def test_calorie_maintenance():
    calculator = CalorieCalculator()

    result = calculator.calculate(
        age=25,
        weight_kg=70,
        height_cm=175,
        sex="male",
        activity_level="moderate",
        fitness_goal="maintenance",
    )

    assert result.bmr == 1673.75
    assert result.maintenance_calories == 2594.31
    assert result.target_calories == 2594.31

    print("Maintenance calorie test: PASSED")


def test_goal_adjustments():
    calculator = CalorieCalculator()

    maintenance = calculator.calculate(
        age=25,
        weight_kg=70,
        height_cm=175,
        sex="male",
        activity_level="moderate",
        fitness_goal="maintenance",
    )

    weight_loss = calculator.calculate(
        age=25,
        weight_kg=70,
        height_cm=175,
        sex="male",
        activity_level="moderate",
        fitness_goal="weight_loss",
    )

    weight_gain = calculator.calculate(
        age=25,
        weight_kg=70,
        height_cm=175,
        sex="male",
        activity_level="moderate",
        fitness_goal="weight_gain",
    )

    muscle_gain = calculator.calculate(
        age=25,
        weight_kg=70,
        height_cm=175,
        sex="male",
        activity_level="moderate",
        fitness_goal="muscle_gain",
    )

    assert (
        weight_loss.target_calories
        == round(
            maintenance.maintenance_calories - 500,
            2,
        )
    )

    assert (
        weight_gain.target_calories
        == round(
            maintenance.maintenance_calories + 300,
            2,
        )
    )

    assert (
        muscle_gain.target_calories
        == round(
            maintenance.maintenance_calories + 300,
            2,
        )
    )

    assert (
        maintenance.target_calories
        == maintenance.maintenance_calories
    )

    print("Goal adjustment test: PASSED")


def test_strength_goal():
    calculator = CalorieCalculator()

    strength = calculator.calculate(
        age=25,
        weight_kg=70,
        height_cm=175,
        sex="male",
        activity_level="moderate",
        fitness_goal="strength",
    )

    muscle_gain = calculator.calculate(
        age=25,
        weight_kg=70,
        height_cm=175,
        sex="male",
        activity_level="moderate",
        fitness_goal="muscle_gain",
    )

    assert (
        strength.target_calories
        == muscle_gain.target_calories
    )

    print("Strength goal test: PASSED")


def test_invalid_sex():
    calculator = CalorieCalculator()

    try:
        calculator.calculate(
            age=25,
            weight_kg=70,
            height_cm=175,
            sex="other",
            activity_level="moderate",
            fitness_goal="maintenance",
        )
    except ValueError:
        print("Invalid sex test: PASSED")
        return

    raise AssertionError(
        "Calorie calculator accepted invalid sex."
    )


def test_invalid_activity_level():
    calculator = CalorieCalculator()

    try:
        calculator.calculate(
            age=25,
            weight_kg=70,
            height_cm=175,
            sex="male",
            activity_level="unknown",
            fitness_goal="maintenance",
        )
    except ValueError:
        print("Invalid activity test: PASSED")
        return

    raise AssertionError(
        "Calorie calculator accepted invalid activity."
    )


def test_invalid_goal():
    calculator = CalorieCalculator()

    try:
        calculator.calculate(
            age=25,
            weight_kg=70,
            height_cm=175,
            sex="male",
            activity_level="moderate",
            fitness_goal="unknown",
        )
    except ValueError:
        print("Invalid goal test: PASSED")
        return

    raise AssertionError(
        "Calorie calculator accepted invalid goal."
    )


def main():
    print("Testing AI Dietician calculations...")
    print()

    test_bmi()
    test_bmi_invalid_weight()
    test_bmi_invalid_height()
    test_calorie_maintenance()
    test_goal_adjustments()
    test_strength_goal()
    test_invalid_sex()
    test_invalid_activity_level()
    test_invalid_goal()

    print()
    print(
        "AI Dietician calculation tests "
        "passed successfully."
    )


if __name__ == "__main__":
    main()
