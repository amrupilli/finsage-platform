from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


ConversationStage = Literal[
    "intro",
    "goal",
    "experience",
    "budget",
    "time_horizon",
    "risk_attitude",
    "complete",
]


class OnboardingSessionCreateResponse(BaseModel):
    session_id: int
    user_id: int
    is_completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class OnboardingMessageCreate(BaseModel):
    message_text: str = Field(..., min_length=1)


class OnboardingMessageResponse(BaseModel):
    role: Literal["assistant", "user"]
    message_text: str


class OnboardingState(BaseModel):
    session_id: int
    current_stage: ConversationStage
    collected_fields: dict[str, str | None]
    missing_fields: list[str]
    is_completed: bool


class OnboardingNextMessageResponse(BaseModel):
    session_id: int
    assistant_message: str
    current_stage: ConversationStage
    missing_fields: list[str]
    is_completed: bool


class OnboardingStartResponse(BaseModel):
    session_id: int
    assistant_message: str
    current_stage: ConversationStage
    missing_fields: list[str]
    is_completed: bool

class OnboardingAnswerResponse(BaseModel):
    answer_id: int
    question_key: str
    field_name: str | None = None
    answer_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class OnboardingAnswersReviewResponse(BaseModel):
    session_id: int
    is_completed: bool
    current_stage: ConversationStage
    missing_fields: list[str]
    collected_fields: dict[str, str | None]
    answers: list[OnboardingAnswerResponse]


class OnboardingAnswerUpdateRequest(BaseModel):
    answer_text: str = Field(..., min_length=1)


class OnboardingAnswerUpdateResponse(BaseModel):
    session_id: int
    answer: OnboardingAnswerResponse
    current_stage: ConversationStage
    missing_fields: list[str]
    collected_fields: dict[str, str | None]
    is_completed: bool
    message: str