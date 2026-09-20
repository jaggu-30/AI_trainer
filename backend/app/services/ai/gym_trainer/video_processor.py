from dataclasses import dataclass
from typing import Callable, Iterator

import cv2
import numpy as np


@dataclass
class VideoFrame:
    frame_number: int
    timestamp_seconds: float
    image: np.ndarray


class GymTrainerVideoProcessor:
    """
    Reads video frames sequentially.

    This class is responsible only for video I/O.
    Pose detection and exercise analysis are handled
    by separate components.
    """

    def __init__(
        self,
        video_path: str,
    ):
        self.video_path = video_path

    def frames(self) -> Iterator[VideoFrame]:
        """
        Yield video frames one at a time.
        """

        capture = cv2.VideoCapture(
            self.video_path
        )

        if not capture.isOpened():
            raise RuntimeError(
                f"Unable to open video: "
                f"{self.video_path}"
            )

        fps = capture.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:
            fps = 30.0

        frame_number = 0

        try:
            while True:
                success, frame = capture.read()

                if not success:
                    break

                timestamp_seconds = (
                    frame_number / fps
                )

                yield VideoFrame(
                    frame_number=frame_number,
                    timestamp_seconds=timestamp_seconds,
                    image=frame,
                )

                frame_number += 1

        finally:
            capture.release()

    def process(
        self,
        callback: Callable[
            [VideoFrame],
            None,
        ],
    ) -> int:
        """
        Process every frame using a callback.

        Returns the total number of processed frames.
        """

        frame_count = 0

        for video_frame in self.frames():
            callback(video_frame)
            frame_count += 1

        return frame_count