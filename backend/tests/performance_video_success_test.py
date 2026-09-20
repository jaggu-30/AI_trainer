from pathlib import Path
import sys
from unittest.mock import patch

import cv2
import numpy as np
from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from ai.gym_trainer.performance_report import (
    PerformanceReportGenerator,
)
from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)
from ai.gym_trainer.video_session_simulator import (
    SquatVideoSessionSimulator,
)

from app.main import app
from app.services.ai.gym_trainer.video_performance_service import (
    VideoPerformanceResult,
)


TEST_EMAIL = "iot-test-user@example.com"
TEST_PASSWORD = "Mypassword123"

VIDEO_PATH = (
    PROJECT_ROOT
    / "ai"
    / "data"
    / "workout"
    / "test_success_video.mp4"
)


class FakeVideoPerformanceService:
    """
    Deterministic replacement for the production
    video-performance service.

    This class is used only inside this test process.
    It generates the same five-repetition performance
    report produced by the simulator.
    """

    def __init__(
        self,
        video_path: str,
    ):
        self.video_path = video_path

    def analyze(
        self,
        exercise: str = "squat",
    ) -> VideoPerformanceResult:
        simulator = SquatVideoSessionSimulator(
            repetitions=5,
            fps=30,
        )

        analyzer = SquatSessionAnalyzer()

        frames = list(
            simulator.frames()
        )

        frame_results = []

        for frame in frames:
            frame_analysis = (
                analyzer.process_frame(
                    frame.landmarks
                )
            )

            if frame_analysis is None:
                continue

            frame_results.append(
                {
                    "frame_number": (
                        frame.frame_number
                    ),
                    "timestamp_seconds": round(
                        frame.timestamp_seconds,
                        3,
                    ),
                    "phase": (
                        frame_analysis.phase
                    ),
                    "repetitions": (
                        frame_analysis.repetitions
                    ),
                    "knee_angle": round(
                        frame_analysis.knee_angle,
                        2,
                    ),
                    "form_score": (
                        frame_analysis.score.overall_score
                    ),
                    "depth_score": (
                        frame_analysis.score.depth_score
                    ),
                    "posture_score": (
                        frame_analysis.score.posture_score
                    ),
                    "control_score": (
                        frame_analysis.score.control_score
                    ),
                    "rating": (
                        frame_analysis.score.rating
                    ),
                    "feedback": (
                        frame_analysis.feedback.messages
                    ),
                }
            )

        summary = analyzer.summary()

        performance = (
            PerformanceReportGenerator().generate(
                summary=summary,
                exercise=exercise.strip().lower(),
            )
        )

        return VideoPerformanceResult(
            exercise=exercise.strip().lower(),
            total_frames=len(frames),
            processed_frames=len(frames),
            detected_frames=len(frames),
            detection_rate=1.0,
            performance=performance,
            frame_results=frame_results,
        )

    def close(self) -> None:
        pass


def create_test_video() -> None:
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
                f"Test frame {frame_number}",
                (40, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2,
            )

            writer.write(frame)

    finally:
        writer.release()


def login(
    client: TestClient,
) -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
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


def get_analytics(
    client: TestClient,
    token: str,
) -> dict:
    response = client.get(
        "/api/v1/analytics/summary",
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        },
    )

    print(
        "Analytics HTTP status:",
        response.status_code,
    )

    response.raise_for_status()

    return response.json()


def test_performance_video_success():
    create_test_video()

    try:
        with TestClient(app) as client:
            token = login(client)

            before_analytics = get_analytics(
                client,
                token,
            )

            before_workouts = (
                before_analytics[
                    "workouts"
                ]["total_workouts"]
            )

            headers = {
                "Authorization": (
                    f"Bearer {token}"
                )
            }

            with patch(
                "app.api.routes.performance."
                "GymTrainerVideoPerformanceService",
                FakeVideoPerformanceService,
            ):

                with VIDEO_PATH.open(
                    "rb"
                ) as video_file:
                    response = client.post(
                        "/api/v1/performance/video",
                        params={
                            "exercise": "squat",
                        },
                        headers=headers,
                        files={
                            "video": (
                                "test_success_video.mp4",
                                video_file,
                                "video/mp4",
                            )
                        },
                    )

            print(
                "Video performance HTTP status:",
                response.status_code,
            )

            print(
                "Response:",
                response.text,
            )

            response.raise_for_status()

            data = response.json()

            assert data["exercise"] == "squat"

            assert (
                data["video"]["total_frames"]
                == 60
            )

            assert (
                data["video"]["processed_frames"]
                == 60
            )

            assert (
                data["video"]["detected_frames"]
                == 60
            )

            assert (
                data["video"]["detection_rate"]
                == 1.0
            )

            assert (
                data["total_repetitions"]
                == 5
            )

            assert (
                data["performance_score"]
                > 0
            )

            assert (
                0
                <= data["depth_score"]
                <= 100
            )

            assert (
                0
                <= data["posture_score"]
                <= 100
            )

            assert (
                0
                <= data["control_score"]
                <= 100
            )

            assert (
                len(
                    data["repetition_scores"]
                )
                == 5
            )

            assert "workout" in data

            assert (
                data["workout"]["exercise"]
                == "squat"
            )

            assert (
                data["workout"][
                    "total_repetitions"
                ]
                == 5
            )

            assert (
                data["workout"][
                    "performance_score"
                ]
                > 0
            )

            after_analytics = get_analytics(
                client,
                token,
            )

            after_workouts = (
                after_analytics[
                    "workouts"
                ]["total_workouts"]
            )

            assert (
                after_workouts
                == before_workouts + 1
            )

            print()
            print(
                "Saved workout ID:",
                data["workout"]["id"],
            )

            print(
                "Saved repetitions:",
                data["workout"][
                    "total_repetitions"
                ],
            )

            print(
                "Saved performance:",
                data["workout"][
                    "performance_score"
                ],
            )

            print(
                "Analytics workouts before:",
                before_workouts,
            )

            print(
                "Analytics workouts after:",
                after_workouts,
            )

            print()
            print(
                "Performance video success "
                "test: PASSED"
            )

    finally:
        if VIDEO_PATH.exists():
            VIDEO_PATH.unlink()


def main():
    test_performance_video_success()


if __name__ == "__main__":
    main()