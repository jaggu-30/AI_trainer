import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_analyzer import SquatFormAnalyzer


def main() -> None:
    analyzer = SquatFormAnalyzer()

    good_depth = analyzer.analyze(
        knee_angle=90.0,
        phase="bottom",
    )

    print("Good-depth test:")
    print("Status:", good_depth.status)
    print("Message:", good_depth.message)
    print("Score:", good_depth.score)

    assert good_depth.status == "good"
    assert good_depth.score == 100

    shallow_depth = analyzer.analyze(
        knee_angle=125.0,
        phase="bottom",
    )

    print()
    print("Shallow-depth test:")
    print("Status:", shallow_depth.status)
    print("Message:", shallow_depth.message)
    print("Score:", shallow_depth.score)

    assert shallow_depth.status == "warning"
    assert shallow_depth.score == 70

    standing = analyzer.analyze(
        knee_angle=175.0,
        phase="standing",
    )

    print()
    print("Standing-position test:")
    print("Status:", standing.status)
    print("Message:", standing.message)
    print("Score:", standing.score)

    assert standing.status == "good"

    print()
    print("Squat form analyzer test passed successfully.")


if __name__ == "__main__":
    main()
