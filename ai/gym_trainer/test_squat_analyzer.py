import sys

sys.path.insert(0, "..")

from ai.gym_trainer.pose import PoseLandmark
from ai.gym_trainer.squat_analyzer import SquatAnalyzer


def create_landmarks(knee_y: float) -> list[PoseLandmark]:
    return [
        PoseLandmark(
            name="LEFT_HIP",
            x=0.50,
            y=0.30,
            z=0.0,
            visibility=1.0,
        ),
        PoseLandmark(
            name="LEFT_KNEE",
            x=0.50,
            y=knee_y,
            z=0.0,
            visibility=1.0,
        ),
        PoseLandmark(
            name="LEFT_ANKLE",
            x=0.50,
            y=0.80,
            z=0.0,
            visibility=1.0,
        ),
    ]


def main() -> None:
    analyzer = SquatAnalyzer()

    standing = create_landmarks(0.55)

    result = analyzer.analyze(standing)

    assert result is not None

    print(
        f"Initial phase: {result.phase}"
    )

    print(
        f"Initial repetitions: {result.repetitions}"
    )

    print()
    print("Squat analyzer initialized successfully.")


if __name__ == "__main__":
    main()
