from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from ai.gym_buddy.memory import (
    ConversationMemoryAnalyzer,
)

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.habit import (
    HabitAnalysisResponse,
    HabitBehaviorResponse,
    HabitMemoryResponse,
    HabitNudgeResponse,
    HabitScheduleResponse,
    HabitSkipRiskResponse,
)
from app.services.ai.habit_tracker_service import (
    HabitTrackerService,
)
from app.services.chat import (
    get_chat_messages,
    list_chat_sessions,
)


router = APIRouter(
    prefix="/api/v1/habits",
    tags=["Habits"],
)


habit_tracker_service = HabitTrackerService()
memory_analyzer = ConversationMemoryAnalyzer()


@router.get(
    "/analysis",
    response_model=HabitAnalysisResponse,
)
def analyze_habits(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Analyze the authenticated user's fitness habits
    using behavioral signals from stored chat history.
    """

    sessions, _ = list_chat_sessions(
        db=db,
        user_id=current_user.id,
        limit=100,
        offset=0,
    )

    messages = []

    for session in sessions:
        messages.extend(
            get_chat_messages(
                db=db,
                session=session,
            )
        )

    conversation_memory = (
        memory_analyzer.analyze(messages)
    )

    analysis = habit_tracker_service.analyze(
        user=current_user,
        memory=conversation_memory,
    )

    return HabitAnalysisResponse(
        memory=HabitMemoryResponse(
            total_messages=(
                analysis.memory.total_messages
            ),
            positive_messages=(
                analysis.memory.positive_messages
            ),
            negative_messages=(
                analysis.memory.negative_messages
            ),
            neutral_messages=(
                analysis.memory.neutral_messages
            ),
            recent_sentiment=(
                analysis.memory.recent_sentiment
            ),
            recent_emotion=(
                analysis.memory.recent_emotion
            ),
            recent_motivation_level=(
                analysis.memory
                .recent_motivation_level
            ),
            unmotivated_count=(
                analysis.memory.unmotivated_count
            ),
            stressed_count=(
                analysis.memory.stressed_count
            ),
            low_motivation_count=(
                analysis.memory
                .low_motivation_count
            ),
            motivation_trend=(
                analysis.memory.motivation_trend
            ),
        ),
        behavior=HabitBehaviorResponse(
            consistency_score=(
                analysis.behavior
                .consistency_score
            ),
            motivation_score=(
                analysis.behavior
                .motivation_score
            ),
            emotional_stability_score=(
                analysis.behavior
                .emotional_stability_score
            ),
            behavioral_risk_score=(
                analysis.behavior
                .behavioral_risk_score
            ),
            risk_level=(
                analysis.behavior.risk_level
            ),
        ),
        skip_risk=HabitSkipRiskResponse(
            probability=(
                analysis.skip_risk.probability
            ),
            level=analysis.skip_risk.level,
            reason=analysis.skip_risk.reason,
        ),
        nudge=HabitNudgeResponse(
            message=analysis.nudge.message,
            urgency=analysis.nudge.urgency,
            action=analysis.nudge.action,
        ),
        schedule=HabitScheduleResponse(
            action=analysis.schedule.action,
            intensity=analysis.schedule.intensity,
            duration_minutes=(
                analysis.schedule.duration_minutes
            ),
            reason=analysis.schedule.reason,
        ),
    )