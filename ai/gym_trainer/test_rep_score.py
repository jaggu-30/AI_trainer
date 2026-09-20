import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_scoring import (
    FormScore,
)
from ai.gym_trainer.rep_score import (
    RepScoreAccumulator,
)


def main():
    print("Testing repetition-level scoring...")
    print()

    accumulator = RepScoreAccumulator()

    scores = [
        FormScore(
            depth_score=90.0,
            posture_score=80.0,
            control_score=85.0,
            overall_score=85.5,
            rating="good",
        ),
        FormScore(
            depth_score=95.0,
            posture_score=85.0,
            control_score=90.0,
            overall_score=90.0,
            rating="excellent",
        ),
        FormScore(
            depth_score=85.0,
            posture_score=75.0,
            control_score=80.0,
            overall_score=80.5,
            rating="good",
        ),
    ]

    for score in scores:
        accumulator.add(score)

    print(
        f"Frames accumulated: "
        f"{accumulator.frame_count}"
    )

    result = accumulator.calculate(
        repetition_number=1
    )

    assert result is not None

    print(
        f"Repetition number: "
        f"{result.repetition_number}"
    )

    print(
        f"Overall score: "
        f"{result.overall_score:.2f}"
    )

    print(
        f"Depth score: "
        f"{result.depth_score:.2f}"
    )

    print(
        f"Posture score: "
        f"{result.posture_score:.2f}"
    )

    print(
        f"Control score: "
        f"{result.control_score:.2f}"
    )

    print(
        f"Rating: "
        f"{result.rating}"
    )

    assert result.repetition_number == 1
    assert result.overall_score == 85.33
    assert result.depth_score == 90.0
    assert result.posture_score == 80.0
    assert result.control_score == 85.0
    assert result.rating == "good"

    accumulator.clear()

    assert accumulator.frame_count == 0
    assert accumulator.is_empty()

    print()
    print(
        "Repetition-level scoring test "
        "passed successfully."
    )


if __name__ == "__main__":
    main()