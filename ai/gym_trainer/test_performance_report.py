from ai.gym_trainer.performance_report import (
    PerformanceReportGenerator,
)
from ai.gym_trainer.simulator import generate_squat_sequence
from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)


def test_performance_report_generation():
    print("Testing performance report generation...")

    analyzer = SquatSessionAnalyzer()

    frames = generate_squat_sequence(repetitions=5)

    for landmarks in frames:
        analyzer.process_frame(landmarks)

    summary = analyzer.summary()

    generator = PerformanceReportGenerator()

    report = generator.generate(
        summary=summary,
        exercise="squat",
    )

    print()
    print(f"Exercise: {report.exercise}")
    print(f"Total repetitions: {report.total_repetitions}")
    print(f"Performance score: {report.performance_score}")
    print(f"Best frame score: {report.best_frame_score}")
    print(f"Worst frame score: {report.worst_frame_score}")
    print(f"Depth score: {report.depth_score}")
    print(f"Posture score: {report.posture_score}")
    print(f"Control score: {report.control_score}")
    print(
        f"Average repetition score: "
        f"{report.average_repetition_score}"
    )
    print(
        f"Best repetition score: "
        f"{report.best_repetition_score}"
    )
    print(
        f"Worst repetition score: "
        f"{report.worst_repetition_score}"
    )
    print(f"Rating: {report.rating}")
    print(f"Warnings: {report.warnings}")

    assert report.exercise == "squat"
    assert report.total_repetitions == 5

    assert report.performance_score > 0
    assert report.best_frame_score >= report.worst_frame_score

    assert report.depth_score >= 0
    assert report.posture_score >= 0
    assert report.control_score >= 0

    assert report.average_repetition_score > 0
    assert report.best_repetition_score > 0
    assert report.worst_repetition_score > 0

    assert report.rating in {
        "excellent",
        "good",
        "needs_improvement",
        "poor",
    }

    assert len(report.repetition_scores) == 5

    print()
    print(
        "Performance report generation test "
        "passed successfully."
    )


def main():
    test_performance_report_generation()


if __name__ == "__main__":
    main()