from pathlib import Path
import sys

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from app.services.ai.gym_trainer.video_processor import (
    GymTrainerVideoProcessor,
)


def create_test_video(
    output_path: Path,
    frame_count: int = 10,
    width: int = 640,
    height: int = 480,
    fps: int = 10,
):
    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        raise RuntimeError(
            "Unable to create test video."
        )

    try:
        for frame_number in range(frame_count):
            frame = np.zeros(
                (height, width, 3),
                dtype=np.uint8,
            )

            cv2.putText(
                frame,
                f"Frame {frame_number}",
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2,
            )

            writer.write(frame)

    finally:
        writer.release()


def test_video_processor():
    print(
        "Testing Gym Trainer video processor..."
    )
    print()

    video_path = (
        PROJECT_ROOT
        / "ai"
        / "data"
        / "workout"
        / "test_video.mp4"
    )

    try:
        create_test_video(video_path)

        print(
            f"Test video: {video_path}"
        )

        processor = GymTrainerVideoProcessor(
            video_path=str(video_path)
        )

        frames = list(processor.frames())

        print(
            f"Frames read: {len(frames)}"
        )

        assert len(frames) == 10

        for index, frame in enumerate(frames):
            assert frame.frame_number == index
            assert frame.image is not None
            assert frame.image.shape == (
                480,
                640,
                3,
            )

        print(
            f"First frame number: "
            f"{frames[0].frame_number}"
        )

        print(
            f"Last frame number: "
            f"{frames[-1].frame_number}"
        )

        print(
            f"Last timestamp: "
            f"{frames[-1].timestamp_seconds:.2f}s"
        )

        processed_frames = []

        processor.process(
            lambda frame: processed_frames.append(
                frame.frame_number
            )
        )

        print(
            f"Callback frames: "
            f"{len(processed_frames)}"
        )

        assert len(processed_frames) == 10

    finally:
        if video_path.exists():
            video_path.unlink()

    print()
    print(
        "Gym Trainer video processor "
        "test passed successfully."
    )


def main():
    test_video_processor()


if __name__ == "__main__":
    main()