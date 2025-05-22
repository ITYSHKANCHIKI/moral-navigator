# backend/app/schemas.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

# ────────── Auth ──────────────────────────────────────────
class Login(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ────────── Tests / Dilemmas ─────────────────────────────
class TestSummary(BaseModel):
    id: int
    title: str
    evaluation: str

    model_config = ConfigDict(from_attributes=True)

class OptionOut(BaseModel):
    id: int
    text: str
    score: int

    model_config = ConfigDict(from_attributes=True)

class DilemmaOut(BaseModel):
    id: int
    text: str
    options: List[OptionOut]

    model_config = ConfigDict(from_attributes=True)


# ────────── History ──────────────────────────────────────
class AnswerCreate(BaseModel):
    dilemma_id: int
    option_id: int

class HistoryCreate(BaseModel):
    test_id: int
    answers: List[AnswerCreate]

class HistoryOut(BaseModel):
    id: int
    user_id: int
    test_id: int
    answers: List[Dict[str, Any]]
    result_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
