import math

from ai.gym_trainer.pose import PoseLandmark


def calculate_angle(
    point_a: PoseLandmark,
    point_b: PoseLandmark,
    point_c: PoseLandmark,
) -> float:
    """
    Calculate the angle ABC in degrees.

    Point B is the vertex of the angle.

    Example:
        point_a = HIP
        point_b = KNEE
        point_c = ANKLE

    Returns:
        Angle in degrees from 0 to 180.
    """
    vector_ba = (
        point_a.x - point_b.x,
        point_a.y - point_b.y,
    )

    vector_bc = (
        point_c.x - point_b.x,
        point_c.y - point_b.y,
    )

    angle_a = math.atan2(
        vector_ba[1],
        vector_ba[0],
    )

    angle_c = math.atan2(
        vector_bc[1],
        vector_bc[0],
    )

    angle = math.degrees(
        angle_c - angle_a
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


def calculate_angle_3d(
    point_a: PoseLandmark,
    point_b: PoseLandmark,
    point_c: PoseLandmark,
) -> float:
    """
    Calculate the 3D angle ABC using x, y and z coordinates.

    This can be useful when a future exercise requires
    depth information from the pose model.
    """
    vector_ba = (
        point_a.x - point_b.x,
        point_a.y - point_b.y,
        point_a.z - point_b.z,
    )

    vector_bc = (
        point_c.x - point_b.x,
        point_c.y - point_b.y,
        point_c.z - point_b.z,
    )

    magnitude_ba = math.sqrt(
        sum(component * component for component in vector_ba)
    )

    magnitude_bc = math.sqrt(
        sum(component * component for component in vector_bc)
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0.0

    dot_product = sum(
        vector_ba[index] * vector_bc[index]
        for index in range(3)
    )

    cosine_angle = dot_product / (
        magnitude_ba * magnitude_bc
    )

    cosine_angle = max(
        -1.0,
        min(1.0, cosine_angle),
    )

    return math.degrees(
        math.acos(cosine_angle)
    )
