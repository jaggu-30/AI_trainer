import sys

import cv2

sys.path.insert(0, "..")

from ai.gym_trainer.pose import PoseDetector


def main() -> None:
    detector = PoseDetector()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        detector.close()
        raise RuntimeError(
            "Could not open the webcam. Check camera permissions and "
            "make sure another application is not using the camera."
        )

    print("Webcam started successfully.")
    print("Press Q to quit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Failed to read a frame from the webcam.")
                break

            landmarks = detector.detect(frame)

            output = detector.draw_landmarks(
                frame,
                landmarks,
            )

            cv2.putText(
                output,
                f"Landmarks: {len(landmarks)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                output,
                "Press Q to quit",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.imshow(
                "AI Gym Trainer - Pose Detection",
                output,
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        detector.close()

    print("Webcam test completed successfully.")


if __name__ == "__main__":
    main()
