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


def main():
    print("Testing MediaPipe with a real image...")
    print()

    image_path = (
        PROJECT_ROOT
        / "ai"
        / "data"
        / "workout"
        / "test_person.png"
    )

    if not image_path.exists():
        print("Test image not found:")
        print(image_path)
        print()
        print(
            "Place a suitable full-body image at this path "
            "and run the test again."
        )
        return

    image = cv2.imread(str(image_path))

    if image is None:
        raise RuntimeError(
            "OpenCV could not read the test image."
        )

    print(f"Image path: {image_path}")
    print(
        f"Image dimensions: "
        f"{image.shape[1]}x{image.shape[0]}"
    )

    processor = GymTrainerFrameProcessor()

    landmarks = processor.process_frame(image)

    print(
        f"Detected landmarks: "
        f"{len(landmarks)}"
    )

    if landmarks:
        print()
        print("Detected landmarks:")

        for landmark in landmarks:
            print(
                f"- {landmark.name}: "
                f"x={landmark.x:.3f}, "
                f"y={landmark.y:.3f}, "
                f"visibility={landmark.visibility:.3f}"
            )

    processor.close()

    if len(landmarks) != 33:
        raise AssertionError(
            f"Expected 33 landmarks, "
            f"but detected {len(landmarks)}."
        )

    print()
    print(
        "MediaPipe real-image test "
        "passed successfully."
    )


if __name__ == "__main__":
    main()