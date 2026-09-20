from pathlib import Path
import sys

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from app.services.ai.gym_trainer.frame_processor import (
    GymTrainerFrameProcessor,
)


def main():
    print("Testing Gym Trainer frame processor...")
    print()

    processor = GymTrainerFrameProcessor()

    print(f"Model path: {processor.model_path}")

    assert Path(processor.model_path).exists()

    print("Pose model exists: yes")

    blank_frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    landmarks = processor.process_frame(
        blank_frame
    )

    print(f"Blank-frame landmarks: {len(landmarks)}")

    assert isinstance(landmarks, list)

    processor.close()

    print()
    print("Gym Trainer frame processor test passed successfully.")


if __name__ == "__main__":
    main()