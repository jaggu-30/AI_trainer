import sys

sys.path.insert(0, "..")

from ai.gym_trainer.squat_analyzer import SquatAnalyzer
from ai.gym_trainer.simulator import create_squat_landmarks


def main():
    analyzer = SquatAnalyzer(
        minimum_visibility=0.5,
        smoothing_alpha=0.6,
    )

    print("Testing integrated squat analyzer...")
    print()

    angles = [
        175.0,
        170.0,
        150.0,
        130.0,
        110.0,
        95.0,
        90.0,
        100.0,
        120.0,
        145.0,
        165.0,
        175.0,
    ]

    for angle in angles:
        landmarks = create_squat_landmarks(angle)

        analysis = analyzer.analyze(landmarks)

        assert analysis is not None

        print(
            f"Input: {angle:>6.1f}° | "
            f"Smoothed: {analysis.knee_angle:>6.1f}° | "
            f"Phase: {analysis.phase:<10} | "
            f"Reps: {analysis.repetitions}"
        )

    assert analyzer.rep_counter.repetitions == 1

    analyzer.reset()

    assert analyzer.rep_counter.repetitions == 0
    assert analyzer.angle_smoother.sample_count == 0

    print()
    print("Integrated squat analyzer test passed successfully.")


if __name__ == "__main__":
    main()