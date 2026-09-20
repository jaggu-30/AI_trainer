import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from ai.gym_trainer.video_session_simulator import (
    SquatVideoSessionSimulator,
)

from app.services.ai.gym_trainer.video_performance_service import (
    GymTrainerVideoPerformanceService,
)


def simulated_landmarks():
    simulator = SquatVideoSessionSimulator(
        repetitions=5,
        fps=30,
    )

    yield from simulator.frames()


def test_video_performance_service():
    service = GymTrainerVideoPerformanceService(
        landmark_provider=lambda _: simulated_landmarks()
    )

    try:
        result = service.analyze(
            exercise="squat"
        )

        assert result.exercise == "squat"

        assert result.total_frames == 60

        assert result.processed_frames == 60

        assert result.detected_frames == 60

        assert result.detection_rate == 1.0

        assert result.performance is not None

        assert (
            result.performance.total_repetitions
            == 5
        )

        assert (
            result.performance.performance_score
            > 0
        )

        assert (
            0
            <= result.performance.depth_score
            <= 100
        )

        assert (
            0
            <= result.performance.posture_score
            <= 100
        )

        assert (
            0
            <= result.performance.control_score
            <= 100
        )

        assert (
            len(
                result.performance.repetition_scores
            )
            == 5
        )

        assert len(
            result.frame_results
        ) > 0

        print(
            f"Frames analyzed: "
            f"{result.total_frames}"
        )

        print(
            f"Frames with pose: "
            f"{result.detected_frames}"
        )

        print(
            f"Repetitions detected: "
            f"{result.performance.total_repetitions}"
        )

        print(
            f"Performance score: "
            f"{result.performance.performance_score}"
        )

        print(
            f"Repetition scores: "
            f"{len(result.performance.repetition_scores)}"
        )

        print(
            "Video performance service "
            "test: PASSED"
        )

    finally:
        service.close()


def main():
    test_video_performance_service()


if __name__ == "__main__":
    main()