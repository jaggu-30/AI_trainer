from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatMessageResponse,
    ChatRequest,
    ChatResponse,
    ChatSessionCreate,
    ChatSessionListResponse,
    ChatSessionResponse,
)
from app.services.ai.dietician.chat_service import DieticianChatService
from app.services.ai.gym_buddy_service import GymBuddyService
from app.services.chat import (
    add_chat_message,
    create_chat_session,
    delete_chat_session,
    get_chat_messages,
    get_chat_session,
    list_chat_sessions,
)

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)


def _session_response(session) -> ChatSessionResponse:
    return ChatSessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


@router.post(
    "/sessions",
    response_model=ChatSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    payload: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = create_chat_session(
        db=db,
        user_id=current_user.id,
        title=payload.title,
    )

    return _session_response(session)


@router.get(
    "/sessions",
    response_model=ChatSessionListResponse,
)
def get_sessions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions, total = list_chat_sessions(
        db=db,
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )

    return ChatSessionListResponse(
        items=[
            _session_response(session)
            for session in sessions
        ],
        total=total,
    )


@router.get(
    "/sessions/{session_id}",
    response_model=ChatHistoryResponse,
)
def get_session_history(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = get_chat_session(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    messages = get_chat_messages(
        db=db,
        session=session,
    )

    return ChatHistoryResponse(
        session=_session_response(session),
        messages=[
            ChatMessageResponse(
                id=message.id,
                session_id=message.session_id,
                role=message.role,
                content=message.content,
                intent=message.intent,
                sentiment=message.sentiment,
                emotion=message.emotion,
                motivation_level=message.motivation_level,
                emotion_confidence=message.emotion_confidence,
                strategy=message.strategy,
                created_at=message.created_at,
            )
            for message in messages
        ],
    )


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = get_chat_session(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    delete_chat_session(
        db=db,
        session=session,
    )

    return None


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = None

    if payload.session_id is not None:
        session = get_chat_session(
            db=db,
            user_id=current_user.id,
            session_id=payload.session_id,
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Chat session not found.",
            )

    if session is None:
        session = create_chat_session(
            db=db,
            user_id=current_user.id,
        )

    # Get previous messages for conversation memory.
    chat_history = get_chat_messages(
        db=db,
        session=session,
    )

    # Analyze sentiment, emotion, motivation,
    # and conversational memory.
    gym_buddy = GymBuddyService()

    buddy_analysis = gym_buddy.analyze(
        user=current_user,
        message=payload.message,
        history=chat_history,
    )

    # Generate the Dietician response.
    try:
        service = DieticianChatService()

        if not current_user.sex:
            raise ValueError(
                "Complete your fitness profile before using the Dietician coach."
            )

        dietician_response, intent = service.respond(
            db=db,
            user=current_user,
            user_message=payload.message,
            sex=current_user.sex,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # Use the Gym Buddy response for emotional
    # and motivational messages.
    if buddy_analysis.response.strategy in {
        "motivation_support",
        "stress_support",
        "positive_reinforcement",
    }:
        response = buddy_analysis.response.message
    else:
        response = dietician_response

    sentiment = buddy_analysis.sentiment.label
    emotion = buddy_analysis.emotion.emotion
    motivation_level = buddy_analysis.emotion.motivation_level
    emotion_confidence = buddy_analysis.emotion.confidence
    strategy = buddy_analysis.response.strategy

    # Store the user message.
    add_chat_message(
        db=db,
        session=session,
        role="user",
        content=payload.message,
        intent=intent,
        sentiment=sentiment,
        emotion=emotion,
        motivation_level=motivation_level,
        emotion_confidence=emotion_confidence,
        strategy=strategy,
    )

    # Store the assistant response.
    assistant_message = add_chat_message(
        db=db,
        session=session,
        role="assistant",
        content=response,
        intent=intent,
        sentiment=sentiment,
        emotion=emotion,
        motivation_level=motivation_level,
        emotion_confidence=emotion_confidence,
        strategy=strategy,
    )

    return ChatResponse(
        session_id=session.id,
        message_id=assistant_message.id,
        message=response,
        intent=intent,
        sentiment=sentiment,
        emotion=emotion,
        motivation_level=motivation_level,
        emotion_confidence=emotion_confidence,
        strategy=strategy,
    )
