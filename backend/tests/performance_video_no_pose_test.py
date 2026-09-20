from pathlib import Path

import cv2
import numpy as np
import requests


BASE_URL = "http://127.0.0.1:8000"

LOGIN_URL = (
    f"{BASE_URL}/api/v1/auth/login"
)

VIDEO_URL = (
    f"{BASE_URL}/api/v1/performance/video"
)

TEST_EMAIL = "iot-test-user@example.com"

TEST_PASSWORD = "Mypassword123"

PROJECT_ROOT = Path(__file__).resolve().parents[2]

VIDEO_PATH = (
    PROJECT_ROOT
    / "ai"
    / "data"
    / "workout"
    / "test_no_pose_video.mp4"
)


def create_test_video():
    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        str(VIDEO_PATH),
        fourcc,
        10,
        (640, 480),
    )

    if not writer.isOpened():
        raise RuntimeError(
            "Unable to create test video."
        )

    try:
        for frame_number in range(10):
            frame = np.zeros(
                (480, 640, 3),
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


def login() -> str:
    response = requests.post(
        LOGIN_URL,
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
        timeout=30,
    )

    print(
        "Login HTTP status:",
        response.status_code,
    )

    response.raise_for_status()

    data = response.json()

    token = data.get("access_token")

    if not token:
        raise RuntimeError(
            "Login succeeded but no access token was returned."
        )

    return token


def test_performance_video_no_pose():
    create_test_video()

    try:
        token = login()

        headers = {
            "Authorization": (
                f"Bearer {token}"
            )
        }

        with VIDEO_PATH.open(
            "rb"
        ) as video_file:
            response = requests.post(
                VIDEO_URL,
                params={
                    "exercise": "squat",
                },
                headers=headers,
                files={
                    "video": (
                        "test_no_pose_video.mp4",
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

        assert response.status_code == 422

        data = response.json()

        assert (
            "No valid human pose"
            in data["detail"]
        )

        print(
            "No-pose performance video "
            "test: PASSED"
        )

    finally:
        if VIDEO_PATH.exists():
            VIDEO_PATH.unlink()


def main():
    test_performance_video_no_pose()


if __name__ == "__main__":
    main()