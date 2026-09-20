from ai.gym_trainer.performance_report import (
    PerformanceReport,
    PerformanceReportGenerator,
)
from ai.gym_trainer.pose import PoseLandmark
from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)


class GymTrainerPerformanceService:
    """
    Service responsible for processing a complete workout
    session and generating a performance report.
    """

    SUPPORTED_EXERCISES = {
        "squat",
    }

    def __init__(self):
        self.report_generator = PerformanceReportGenerator()

    def analyze(
        self,
        exercise: str,
        frames: list[list],
    ) -> PerformanceReport:
        """
        Analyze a complete sequence of pose landmark frames.
        """

        normalized_exercise = exercise.strip().lower()

        if normalized_exercise not in self.SUPPORTED_EXERCISES:
            raise ValueError(
                f"Unsupported exercise: {exercise}"
            )

        if not frames:
            raise ValueError(
                "At least one frame is required."
            )

        if normalized_exercise == "squat":
            return self._analyze_squat(
                frames=frames,
            )

        raise ValueError(
            f"Unsupported exercise: {exercise}"
        )

    def _analyze_squat(
        self,
        frames: list[list],
    ) -> PerformanceReport:
        """
        Process squat frames and generate the final
        performance report.
        """

        analyzer = SquatSessionAnalyzer()

        try:
            for frame in frames:
                landmarks = self._convert_landmarks(
                    frame
                )

                analyzer.process_frame(
                    landmarks
                )

            summary = analyzer.summary()

            return self.report_generator.generate(
                summary=summary,
                exercise="squat",
            )

        finally:
            analyzer.reset()

    @staticmethod
    def _convert_landmarks(
        frame: list,
    ) -> list[PoseLandmark]:
        """
        Convert API landmark objects into the internal
        PoseLandmark representation.
        """

        landmarks = []

        for landmark in frame:
            if isinstance(landmark, PoseLandmark):
                landmarks.append(landmark)
                continue

            landmarks.append(
                PoseLandmark(
                    name=landmark.name,
                    x=landmark.x,
                    y=landmark.y,
                    z=landmark.z,
                    visibility=landmark.visibility,
                )
            )

        return landmarks