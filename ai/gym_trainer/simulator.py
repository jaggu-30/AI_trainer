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


def _point_from_angle(
    origin_x: float,
    origin_y: float,
    length: float,
    angle_degrees: float,
) -> tuple[float, float]:
    """
    Create a 2D point from an origin, length and angle.
    """

    angle_radians = math.radians(angle_degrees)

    return (
        origin_x + length * math.cos(angle_radians),
        origin_y + length * math.sin(angle_radians),
    )


def create_squat_landmarks(
    knee_angle: float,
    torso_lean: float = 10.0,
) -> list[PoseLandmark]:
    """
    Generate a synthetic side-view squat pose.

    knee_angle:
        Angle at the knee in degrees.

    torso_lean:
        Forward torso inclination in degrees.
        0 means vertical torso.
    """

    if not 0 < knee_angle < 180:
        raise ValueError(
            "knee_angle must be between 0 and 180 degrees."
        )

    # -----------------------------
    # Main body dimensions
    # -----------------------------

    hip_x = 0.50
    hip_y = 0.45

    thigh_length = 0.25
    shin_length = 0.25
    torso_length = 0.30

    # -----------------------------
    # Knee position
    # -----------------------------

    # The thigh points downward.
    thigh_direction = 90.0

    knee_x, knee_y = _point_from_angle(
        hip_x,
        hip_y,
        thigh_length,
        thigh_direction,
    )

    # -----------------------------
    # Ankle position
    # -----------------------------

    # Create the lower-leg direction so that
    # the requested angle exists at the knee.
    shin_direction = 270.0 + knee_angle

    ankle_x, ankle_y = _point_from_angle(
        knee_x,
        knee_y,
        shin_length,
        shin_direction,
    )

    # -----------------------------
    # Shoulder position
    # -----------------------------

    torso_direction = -90.0 + torso_lean

    shoulder_x, shoulder_y = _point_from_angle(
        hip_x,
        hip_y,
        torso_length,
        torso_direction,
    )

    # -----------------------------
    # Build the synthetic skeleton
    # -----------------------------

    positions = {
        "LEFT_SHOULDER": (
            shoulder_x,
            shoulder_y,
        ),
        "LEFT_HIP": (
            hip_x,
            hip_y,
        ),
        "LEFT_KNEE": (
            knee_x,
            knee_y,
        ),
        "LEFT_ANKLE": (
            ankle_x,
            ankle_y,
        ),
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
    Generate a clean synthetic squat sequence.
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
def generate_variable_squat_sequence(
    repetitions: list[dict],
) -> list[list[PoseLandmark]]:
    """
    Generate squat frames with different form characteristics
    for each repetition.

    Each repetition dictionary may contain:
        knee_angle: list[float]
        torso_lean: float
    """

    if not repetitions:
        raise ValueError(
            "repetitions must contain at least one repetition."
        )

    sequence = []

    for repetition in repetitions:
        knee_angles = repetition.get(
            "knee_angle"
        )

        torso_lean = repetition.get(
            "torso_lean",
            10.0,
        )

        if not knee_angles:
            raise ValueError(
                "Each repetition must contain "
                "at least one knee angle."
            )

        for knee_angle in knee_angles:
            sequence.append(
                create_squat_landmarks(
                    knee_angle=knee_angle,
                    torso_lean=torso_lean,
                )
            )

    return sequence