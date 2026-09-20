from datetime import date

from pydantic import BaseModel


class WeeklyPerformanceResponse(BaseModel):
    week_start: date
    week_end: date

    workout_count: int
    total_repetitions: int

    average_performance_score: float
    best_performance_score: float
    worst_performance_score: float

    average_depth_score: float
    average_posture_score: float
    average_control_score: float

    performance_trend: str
    summary: str