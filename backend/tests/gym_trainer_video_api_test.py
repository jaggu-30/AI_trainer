from pathlib import Path

import cv2
import numpy as np
import requests


BASE_URL = "http://127.0.0.1:8000"
VIDEO_URL = (
    f"{BASE_URL}/api/v1/gym-trainer/video"
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEO_PATH = (
    PROJECT_ROOT
    / "ai"
    / "data"
    / "workout"
    / "test_video.mp4"
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
        for frame_number in range(
            frame_count
        ):
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


def test_gym_trainer_video_api():
    create_test_video(VIDEO_PATH)

    try:
        with VIDEO_PATH.open(
            "rb"
        ) as video_file:
            response = requests.post(
                VIDEO_URL,
                params={
                    "exercise": "squat",
                },
                files={
                    "video": (
                        "test_video.mp4",
                        video_file,
                        "video/mp4",
                    )
                },
                timeout=120,
            )

        print(
            "HTTP status:",
            response.status_code,
        )

        print(
            "Response:",
            response.text,
        )

        response.raise_for_status()

        data = response.json()

        assert data["exercise"] == "squat"
        assert data["total_frames"] == 10
        assert data["processed_frames"] == 10

        # The synthetic video contains no person.
        assert data["detected_frames"] == 0
        assert data["detection_rate"] == 0.0
        assert data["results"] == []

        print()
        print(
            "Gym Trainer video API "
            "test: PASSED"
        )

    finally:
        if VIDEO_PATH.exists():
            VIDEO_PATH.unlink()


if __name__ == "__main__":
    test_gym_trainer_video_api()