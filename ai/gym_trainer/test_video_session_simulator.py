from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from ai.gym_trainer.video_session_simulator import (
    SquatVideoSessionSimulator,
)

from app.services.ai.gym_trainer.service import (
    GymTrainerService,
)


def main():
    print(
        "Testing continuous squat video simulation..."
    )
    print()

    simulator = SquatVideoSessionSimulator(
        repetitions=5,
        fps=30.0,
    )

    trainer = GymTrainerService()

    processed_frames = 0
    final_repetitions = 0
    scores = []

    for frame in simulator.frames():
        result = trainer.process(
            exercise="squat",
            landmarks=frame.landmarks,
        )

        processed_frames += 1

        if result is not None:
            final_repetitions = result[
                "repetitions"
            ]

            scores.append(
                result["form_score"]
            )

    print(
        f"Processed frames: "
        f"{processed_frames}"
    )

    print(
        f"Expected repetitions: 5"
    )

    print(
        f"Detected repetitions: "
        f"{final_repetitions}"
    )

    print(
        f"Scored frames: "
        f"{len(scores)}"
    )

    if scores:
        average_score = (
            sum(scores) / len(scores)
        )

        print(
            f"Average frame score: "
            f"{average_score:.2f}"
        )

    assert processed_frames == 60
    assert final_repetitions == 5
    assert len(scores) == 60

    print()
    print(
        "Continuous squat video simulation "
        "test passed successfully."
    )


if __name__ == "__main__":
    main()