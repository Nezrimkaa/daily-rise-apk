from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# === User ===
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# === Token ===
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# === Habit ===
class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_quantitative: bool = False
    target_value: int = 1
    unit: Optional[str] = None


class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class HabitResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    user_id: int
    is_quantitative: bool = False
    target_value: int = 0
    unit: Optional[str] = None

    model_config = {"from_attributes": True}


class HabitWithLogs(HabitResponse):
    logs: list["HabitLogResponse"] = []
    today_value: int = 0  # Сумма за сегодня


# === HabitLog ===
class HabitLogCreate(BaseModel):
    habit_id: int
    value: int = 1


class HabitLogResponse(BaseModel):
    id: int
    date: datetime
    value: int

    model_config = {"from_attributes": True}


# === Stats ===
class HabitStats(BaseModel):
    habit_id: int
    title: str
    total_completions: int
    current_streak: int
    completion_rate: float
    is_quantitative: bool = False
    target_value: int = 1
    unit: Optional[str] = None
    today_value: int = 0
    progress_percent: int = 0
