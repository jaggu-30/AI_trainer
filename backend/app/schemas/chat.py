from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: int | None = Field(default=None, ge=1)


class ChatResponse(BaseModel):
    session_id: int
    message_id: int
    message: str
    intent: str
    sentiment: str | None = None
    emotion: str | None = None
    motivation_level: str | None = None
    emotion_confidence: float | None = None
    strategy: str | None = None


class ChatSessionCreate(BaseModel):
    title: str | None = Field(default=None, max_length=200)


class ChatSessionResponse(BaseModel):
    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime


class ChatSessionListResponse(BaseModel):
    items: list[ChatSessionResponse]
    total: int


class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    intent: str | None
    sentiment: str | None
    emotion: str | None
    motivation_level: str | None
    emotion_confidence: float | None
    strategy: str | None
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    session: ChatSessionResponse
    messages: list[ChatMessageResponse]
