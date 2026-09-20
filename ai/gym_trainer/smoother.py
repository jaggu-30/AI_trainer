class AngleSmoother:
    """
    Smooth joint-angle measurements using an Exponential Moving Average.

    EMA gives more weight to recent measurements, which reduces noise
    while introducing less delay than a simple moving average.
    """

    def __init__(self, alpha: float = 0.6):
        if not 0.0 < alpha <= 1.0:
            raise ValueError(
                "alpha must be greater than 0.0 and less than or equal to 1.0."
            )

        self.alpha = alpha
        self._smoothed_angle: float | None = None

    def update(self, angle: float) -> float:
        """
        Add a new angle and return the smoothed angle.
        """

        angle = float(angle)

        if self._smoothed_angle is None:
            self._smoothed_angle = angle
        else:
            self._smoothed_angle = (
                self.alpha * angle
                + (1.0 - self.alpha) * self._smoothed_angle
            )

        return self._smoothed_angle

    def reset(self):
        """
        Clear the smoothing state.
        """

        self._smoothed_angle = None

    @property
    def sample_count(self) -> int:
        """
        Return 1 when the smoother has received data,
        otherwise 0.
        """

        return 0 if self._smoothed_angle is None else 1