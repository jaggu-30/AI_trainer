import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_analyzer import SquatFormAnalyzer
from ai.gym_trainer.squat_analyzer import SquatAnalyzer
from ai.gym_trainer.simulator import generate_squat_sequence


def main() -> None:
    squat_analyzer = SquatAnalyzer()
    form_analyzer = SquatFormAnalyzer()

    sequence = generate_squat_sequence(
        repetitions=10
    )

    print("Starting AI Gym Trainer simulation...")
    print()
    print("Expected repetitions: 10")
    print()

    last_phase = None

    for frame_number, landmarks in enumerate(
        sequence,
        start=1,
    ):
        analysis = squat_analyzer.analyze(
            landmarks
        )

        if analysis is None:
            continue

        if analysis.phase != last_phase:
            print(
                f"Frame {frame_number:>3} | "
                f"Phase: {analysis.phase:<10} | "
                f"Knee: {analysis.knee_angle:>6.1f}° | "
                f"Reps: {analysis.repetitions}"
            )

            last_phase = analysis.phase

        form = form_analyzer.analyze(
            knee_angle=analysis.knee_angle,
            phase=analysis.phase,
        )

    final_reps = squat_analyzer.rep_counter.repetitions

    print()
    print("Simulation completed.")
    print("Expected repetitions:", 10)
    print("Detected repetitions:", final_reps)

    assert final_reps == 10

    print()
    print(
        "AI Gym Trainer full pipeline test passed successfully."
    )


if __name__ == "__main__":
    main()
