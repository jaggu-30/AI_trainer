import sys

sys.path.insert(0, "..")

from ai.gym_trainer.landmark_filter import LandmarkFilter
from ai.gym_trainer.pose import PoseLandmark


def main():
    landmarks = [
        PoseLandmark(
            name="LEFT_HIP",
            x=0.5,
            y=0.3,
            z=0.0,
            visibility=0.95,
        ),
        PoseLandmark(
            name="LEFT_KNEE",
            x=0.5,
            y=0.55,
            z=0.0,
            visibility=0.90,
        ),
        PoseLandmark(
            name="LEFT_ANKLE",
            x=0.6,
            y=0.55,
            z=0.0,
            visibility=0.30,
        ),
    ]

    landmark_filter = LandmarkFilter(minimum_visibility=0.5)

    filtered = landmark_filter.filter(landmarks)

    print("Testing landmark confidence filter...")
    print()

    for landmark in landmarks:
        status = (
            "ACCEPTED"
            if landmark in filtered
            else "REJECTED"
        )

        print(
            f"{landmark.name:<15} "
            f"Visibility: {landmark.visibility:.2f} "
            f"→ {status}"
        )

    assert len(filtered) == 2

    required = (
        "LEFT_HIP",
        "LEFT_KNEE",
        "LEFT_ANKLE",
    )

    assert not landmark_filter.has_required_landmarks(
        landmarks,
        required,
    )

    print()
    print("Landmark confidence filter test passed successfully.")


if __name__ == "__main__":
    main()