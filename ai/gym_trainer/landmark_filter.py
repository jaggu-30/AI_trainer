from ai.gym_trainer.pose import PoseLandmark


class LandmarkFilter:
    """
    Filters pose landmarks using their visibility/confidence value.
    """

    def __init__(self, minimum_visibility: float = 0.5):
        if not 0.0 <= minimum_visibility <= 1.0:
            raise ValueError(
                "minimum_visibility must be between 0.0 and 1.0."
            )

        self.minimum_visibility = minimum_visibility

    def is_visible(self, landmark: PoseLandmark) -> bool:
        return landmark.visibility >= self.minimum_visibility

    def filter(self, landmarks: list[PoseLandmark]) -> list[PoseLandmark]:
        return [
            landmark
            for landmark in landmarks
            if self.is_visible(landmark)
        ]

    def has_required_landmarks(
        self,
        landmarks: list[PoseLandmark],
        required_names: tuple[str, ...],
    ) -> bool:
        landmark_map = {
            landmark.name: landmark
            for landmark in landmarks
        }

        return all(
            name in landmark_map
            and self.is_visible(landmark_map[name])
            for name in required_names
        )