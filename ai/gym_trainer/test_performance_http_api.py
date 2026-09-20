import requests

from ai.gym_trainer.simulator import (
    generate_squat_sequence,
)


API_URL = (
    "http://127.0.0.1:8000"
    "/api/v1/gym-trainer/performance"
)


def main():
    print("Testing Gym Trainer Performance HTTP API...")

    landmarks_sequence = generate_squat_sequence(
        repetitions=5
    )

    frames = []

    for landmarks in landmarks_sequence:
        frame = []

        for landmark in landmarks:
            frame.append(
                {
                    "name": landmark.name,
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z,
                    "visibility": landmark.visibility,
                }
            )

        frames.append(frame)

    payload = {
        "exercise": "squat",
        "frames": frames,
    }

    print(f"Sending frames: {len(frames)}")
    print(
        f"Landmarks per frame: "
        f"{len(frames[0])}"
    )

    response = requests.post(
        API_URL,
        json=payload,
        timeout=60,
    )

    print(
        f"HTTP status: "
        f"{response.status_code}"
    )

    response.raise_for_status()

    data = response.json()

    print()
    print(f"Exercise: {data['exercise']}")
    print(
        f"Total repetitions: "
        f"{data['total_repetitions']}"
    )
    print(
        f"Performance score: "
        f"{data['performance_score']}"
    )
    print(
        f"Best frame score: "
        f"{data['best_frame_score']}"
    )
    print(
        f"Worst frame score: "
        f"{data['worst_frame_score']}"
    )
    print(
        f"Depth score: "
        f"{data['depth_score']}"
    )
    print(
        f"Posture score: "
        f"{data['posture_score']}"
    )
    print(
        f"Control score: "
        f"{data['control_score']}"
    )
    print(
        f"Average repetition score: "
        f"{data['average_repetition_score']}"
    )
    print(
        f"Best repetition score: "
        f"{data['best_repetition_score']}"
    )
    print(
        f"Worst repetition score: "
        f"{data['worst_repetition_score']}"
    )
    print(f"Rating: {data['rating']}")

    print()
    print("Repetition scores:")

    for repetition in data["repetition_scores"]:
        print(
            f"- Rep "
            f"{repetition['repetition_number']}: "
            f"{repetition['overall_score']} "
            f"({repetition['rating']})"
        )

    print()
    print(
        f"Warnings: "
        f"{data['warnings']}"
    )

    assert data["exercise"] == "squat"

    assert (
        data["total_repetitions"] == 5
    )

    assert (
        data["performance_score"] > 0
    )

    assert (
        0 <= data["best_frame_score"] <= 100
    )

    assert (
        0 <= data["worst_frame_score"] <= 100
    )

    assert (
        0 <= data["depth_score"] <= 100
    )

    assert (
        0 <= data["posture_score"] <= 100
    )

    assert (
        0 <= data["control_score"] <= 100
    )

    assert (
        len(data["repetition_scores"]) == 5
    )

    print()
    print(
        "Gym Trainer Performance HTTP API "
        "test passed successfully."
    )


if __name__ == "__main__":
    main()