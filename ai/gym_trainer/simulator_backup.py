import math

from ai.gym_trainer.pose import PoseLandmark


LANDMARK_NAMES = [
    "NOSE",
    "LEFT_EYE_INNER",
    "LEFT_EYE",
    "LEFT_EYE_OUTER",
    "RIGHT_EYE_INNER",
    "RIGHT_EYE",
    "RIGHT_EYE_OUTER",
    "LEFT_EAR",
    "RIGHT_EAR",
    "MOUTH_LEFT",
    "MOUTH_RIGHT",
    "LEFT_SHOULDER",
    "RIGHT_SHOULDER",
    "LEFT_ELBOW",
    "RIGHT_ELBOW",
    "LEFT_WRIST",
    "RIGHT_WRIST",
    "LEFT_PINKY",
    "RIGHT_PINKY",
    "LEFT_INDEX",
    "RIGHT_INDEX",
    "LEFT_THUMB",
    "RIGHT_THUMB",
    "LEFT_HIP",
    "RIGHT_HIP",
    "LEFT_KNEE",
    "RIGHT_KNEE",
    "LEFT_ANKLE",
    "RIGHT_ANKLE",
    "LEFT_HEEL",
    "RIGHT_HEEL",
    "LEFT_FOOT_INDEX",
    "RIGHT_FOOT_INDEX",
]


def create_squat_landmarks(
    knee_angle: float,
) -> list[PoseLandmark]:
    """
    Generate synthetic landmarks whose measured knee angle
    matches the requested angle.

    The left knee is the angle vertex:

        LEFT_HIP
             \
              \
           LEFT_KNEE
                 \
                  \
               LEFT_ANKLE
    """

    if not 0 < knee_angle < 180:
        raise ValueError(
            "knee_angle must be between 0 and 180 degrees."
        )

    # Keep the hip and knee fixed.
    hip_x = 0.50
    hip_y = 0.30

    knee_x = 0.50
    knee_y = 0.55

    # Vector from knee toward hip.
    hip_vector = (
        hip_x - knee_x,
        hip_y - knee_y,
    )

    # We need the ankle vector to form the requested
    # angle with the knee-to-hip vector.
    #
    # The hip vector points upward.
    # Rotate it clockwise by the requested angle.

    hip_direction = math.atan2(
        hip_vector[1],
        hip_vector[0],
    )

    ankle_direction = (
        hip_direction + math.radians(knee_angle)
    )

    ankle_length = 0.25

    ankle_x = (
        knee_x
        + ankle_length * math.cos(ankle_direction)
    )

    ankle_y = (
        knee_y
        + ankle_length * math.sin(ankle_direction)
    )

    positions = {
        "LEFT_HIP": (hip_x, hip_y),
        "LEFT_KNEE": (knee_x, knee_y),
        "LEFT_ANKLE": (ankle_x, ankle_y),
    }

    landmarks = []

    for name in LANDMARK_NAMES:
        x, y = positions.get(
            name,
            (0.5, 0.5),
        )

        landmarks.append(
            PoseLandmark(
                name=name,
                x=x,
                y=y,
                z=0.0,
                visibility=1.0,
            )
        )

    return landmarks


def generate_squat_sequence(
    repetitions: int = 5,
) -> list[list[PoseLandmark]]:
    """
    Generate complete synthetic squat repetitions.

    Each repetition contains:

        standing
            ↓
        descending
            ↓
        bottom
            ↓
        ascending
            ↓
        standing
    """

    if repetitions < 1:
        raise ValueError(
            "repetitions must be at least 1."
        )

    sequence = []

    movement_angles = [
        175,
        165,
        150,
        130,
        110,
        95,
        90,
        100,
        120,
        145,
        165,
        175,
    ]

    for _ in range(repetitions):
        for angle in movement_angles:
            sequence.append(
                create_squat_landmarks(angle)
            )

    return sequence
