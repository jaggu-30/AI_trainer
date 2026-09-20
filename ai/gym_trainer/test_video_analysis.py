from pathlib import Path
import sys

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from app.services.ai.gym_trainer.video_analysis import (
    GymTrainerVideoAnalysisService,
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


def test_video_analysis_integration():
    print(
        "Testing video analysis integration..."
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

        service = GymTrainerVideoAnalysisService(
            video_path=str(video_path)
        )

        result = service.analyze(
            exercise="squat"
        )

        print(
            f"Total frames: "
            f"{result.total_frames}"
        )

        print(
            f"Processed frames: "
            f"{result.processed_frames}"
        )

        print(
            f"Detected frames: "
            f"{result.detected_frames}"
        )

        print(
            f"Analysis results: "
            f"{len(result.results)}"
        )

        assert result.total_frames == 10
        assert result.processed_frames == 10

        # The synthetic test video contains
        # no human body, so no pose should be detected.
        assert result.detected_frames == 0
        assert len(result.results) == 0

    finally:
        if video_path.exists():
            video_path.unlink()

    print()
    print(
        "Video analysis integration test "
        "passed successfully."
    )


def main():
    test_video_analysis_integration()


if __name__ == "__main__":
    main()