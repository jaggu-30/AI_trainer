import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_scoring import FormScore
from ai.gym_trainer.rep_score import RepScoreAccumulator


def create_score(
    overall_score: float,
) -> FormScore:
    return FormScore(
        depth_score=overall_score,
        posture_score=overall_score,
        control_score=overall_score,
        overall_score=overall_score,
        rating="good",
    )


def main():
    print("Testing multiple repetition scores...")
    print()

    accumulator = RepScoreAccumulator()

    repetition_scores = [
        [85.0, 85.0, 85.0],
        [92.0, 92.0, 92.0],
        [74.0, 74.0, 74.0],
        [88.0, 88.0, 88.0],
        [95.0, 95.0, 95.0],
    ]

    expected_scores = [
        85.0,
        92.0,
        74.0,
        88.0,
        95.0,
    ]

    results = []

    for repetition_number, frame_scores in enumerate(
        repetition_scores,
        start=1,
    ):
        accumulator.clear()

        for frame_score in frame_scores:
            accumulator.add(
                create_score(frame_score)
            )

        result = accumulator.calculate(
            repetition_number=repetition_number
        )

        assert result is not None

        results.append(result)

        print(
            f"Rep {repetition_number}: "
            f"{result.overall_score:.2f} "
            f"({result.rating})"
        )

        assert (
            result.overall_score
            == expected_scores[
                repetition_number - 1
            ]
        )

    print()

    assert len(results) == 5

    assert [
        result.overall_score
        for result in results
    ] == expected_scores

    print(
        "All five repetition scores were "
        "calculated independently."
    )

    print()
    print(
        "Multiple repetition scoring test "
        "passed successfully."
    )


if __name__ == "__main__":
    main()