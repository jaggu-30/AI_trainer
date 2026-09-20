from datetime import datetime

from sqlalchemy.orm import Session

from app.models.chat import ChatMessage, ChatSession


def create_chat_session(
    db: Session,
    user_id: int,
    title: str | None = None,
) -> ChatSession:
    session = ChatSession(
        user_id=user_id,
        title=title or "Fitness Assistant Chat",
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_chat_session(
    db: Session,
    user_id: int,
    session_id: int,
) -> ChatSession | None:
    return (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id,
        )
        .first()
    )


def list_chat_sessions(
    db: Session,
    user_id: int,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[ChatSession], int]:
    query = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
    )

    total = query.count()
    sessions = query.offset(offset).limit(limit).all()

    return sessions, total


def add_chat_message(
    db: Session,
    session: ChatSession,
    role: str,
    content: str,
    intent: str | None = None,
    sentiment: str | None = None,
    emotion: str | None = None,
    motivation_level: str | None = None,
    emotion_confidence: float | None = None,
    strategy: str | None = None,
) -> ChatMessage:
    message = ChatMessage(
        session_id=session.id,
        role=role,
        content=content,
        intent=intent,
        sentiment=sentiment,
        emotion=emotion,
        motivation_level=motivation_level,
        emotion_confidence=emotion_confidence,
        strategy=strategy,
    )

    db.add(message)

    now = datetime.utcnow()
    message.created_at = now
    session.updated_at = now

    db.commit()
    db.refresh(message)

    return message


def get_chat_messages(
    db: Session,
    session: ChatSession,
) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id)
        .order_by(
            ChatMessage.created_at.asc(),
            ChatMessage.id.asc(),
        )
        .all()
    )


def delete_chat_session(
    db: Session,
    session: ChatSession,
) -> None:
    db.delete(session)
    db.commit()