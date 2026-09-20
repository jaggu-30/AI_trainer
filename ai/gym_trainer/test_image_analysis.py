from pathlib import Path
import sys

import cv2


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from app.services.ai.gym_trainer.frame_processor import (
    GymTrainerFrameProcessor,
)
from app.services.ai.gym_trainer.service import (
    GymTrainerService,
)


def main():
    print("Testing complete image analysis pipeline...")
    print()

    image_path = (
        PROJECT_ROOT
        / "ai"
        / "data"
        / "workout"
        / "test_person.png"
    )

    if not image_path.exists():
        raise FileNotFoundError(
            f"Test image not found: {image_path}"
        )

    image = cv2.imread(str(image_path))

    if image is None:
        raise RuntimeError(
            "OpenCV could not read the test image."
        )

    print(
        f"Image: "
        f"{image.shape[1]}x{image.shape[0]}"
    )

    frame_processor = GymTrainerFrameProcessor()
    trainer_service = GymTrainerService()

    landmarks = frame_processor.process_frame(image)

    print(
        f"Detected landmarks: "
        f"{len(landmarks)}"
    )

    assert len(landmarks) == 33

    result = trainer_service.process(
        exercise="squat",
        landmarks=landmarks,
    )

    if result is None:
        raise RuntimeError(
            "Gym Trainer could not analyze the detected pose."
        )

    print()
    print("AI analysis result:")
    print(f"Exercise: {result['exercise']}")
    print(f"Knee angle: {result['knee_angle']}")
    print(f"Phase: {result['phase']}")
    print(f"Repetitions: {result['repetitions']}")
    print(f"Depth score: {result['depth_score']}")
    print(f"Posture score: {result['posture_score']}")
    print(f"Control score: {result['control_score']}")
    print(f"Form score: {result['form_score']}")
    print(f"Rating: {result['rating']}")

    print()
    print("Feedback:")

    for message in result["feedback"]:
        print(f"- {message}")

    frame_processor.close()

    assert result["exercise"] == "squat"
    assert result["repetitions"] >= 0
    assert 0 <= result["form_score"] <= 100
    assert result["rating"] in {
        "excellent",
        "good",
        "needs_improvement",
        "poor",
    }
    assert len(result["feedback"]) > 0

    print()
    print(
        "Complete image analysis pipeline "
        "test passed successfully."
    )


if __name__ == "__main__":
    main()