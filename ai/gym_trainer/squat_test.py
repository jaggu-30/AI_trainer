import sys

import cv2

sys.path.insert(0, "..")

from ai.gym_trainer.form_analyzer import SquatFormAnalyzer
from ai.gym_trainer.pose import PoseDetector
from ai.gym_trainer.squat_analyzer import SquatAnalyzer


def main() -> None:
    detector = PoseDetector()
    squat_analyzer = SquatAnalyzer()
    form_analyzer = SquatFormAnalyzer()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        detector.close()
        raise RuntimeError(
            "Could not open the webcam. "
            "Check camera permissions and make sure another "
            "application is not using the camera."
        )

    print("AI Squat Trainer started.")
    print("Perform slow squats.")
    print("Press Q to quit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Failed to read webcam frame.")
                break

            landmarks = detector.detect(frame)

            output = detector.draw_landmarks(
                frame,
                landmarks,
            )

            # Basic information.
            cv2.putText(
                output,
                f"Landmarks: {len(landmarks)}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2,
            )

            analysis = squat_analyzer.analyze(
                landmarks
            )

            if analysis is not None:
                form = form_analyzer.analyze(
                    knee_angle=analysis.knee_angle,
                    phase=analysis.phase,
                )

                cv2.putText(
                    output,
                    "Exercise: SQUAT",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    output,
                    f"Phase: {analysis.phase.upper()}",
                    (20, 105),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    output,
                    f"Reps: {analysis.repetitions}",
                    (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    output,
                    f"Knee Angle: {analysis.knee_angle:.1f}",
                    (20, 175),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    output,
                    f"Form: {form.status.upper()}",
                    (20, 210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    output,
                    f"Score: {form.score}",
                    (20, 245),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

                # Feedback message.
                cv2.putText(
                    output,
                    form.message,
                    (20, 285),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

            else:
                cv2.putText(
                    output,
                    "No complete pose detected",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

            cv2.putText(
                output,
                "Press Q to quit",
                (20, output.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2,
            )

            cv2.imshow(
                "AI Gym Trainer - Squat Analysis",
                output,
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        detector.close()

    print()
    print("AI Squat Trainer stopped successfully.")
    print(
        "Final repetitions:",
        squat_analyzer.rep_counter.repetitions,
    )


if __name__ == "__main__":
    main()
