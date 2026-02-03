from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.enums import WorkoutType, WorkoutStatus, MediaType

# ==================== Workout Schemas ====================

class WorkoutBase(BaseModel):
    workout_datetime: datetime
    workout_type: WorkoutType
    duration_minutes: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    status: WorkoutStatus = WorkoutStatus.COMPLETED

class WorkoutCreate(WorkoutBase):
    user_id: int

class WorkoutUpdate(BaseModel):
    workout_datetime: Optional[datetime] = None
    workout_type: Optional[WorkoutType] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[WorkoutStatus] = None

class WorkoutResponse(WorkoutBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

# ==================== Strength Exercise Schemas ====================

class StrengthExerciseBase(BaseModel):
    exercise_name: str
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    rpe: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    order_index: int = 0


class StrengthExerciseCreate(StrengthExerciseBase):
    workout_id: int


class StrengthExerciseUpdate(BaseModel):
    exercise_name: Optional[str] = None
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    rpe: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    order_index: Optional[int] = None


class StrengthExerciseResponse(StrengthExerciseBase):
    id: int
    workout_id: int
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)


# ==================== Cardio Activity Schemas ====================

class CardioActivityBase(BaseModel):
    activity_type: str
    distance_km: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    avg_pace_min_per_km: Optional[float] = Field(None, ge=0)
    avg_heart_rate: Optional[int] = Field(None, ge=0, le=250)
    max_heart_rate: Optional[int] = Field(None, ge=0, le=250)
    calories_burned: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class CardioActivityCreate(CardioActivityBase):
    workout_id: int


class CardioActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    distance_km: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    avg_pace_min_per_km: Optional[float] = Field(None, ge=0)
    avg_heart_rate: Optional[int] = Field(None, ge=0, le=250)
    max_heart_rate: Optional[int] = Field(None, ge=0, le=250)
    calories_burned: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class CardioActivityResponse(CardioActivityBase):
    id: int
    workout_id: int
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

# ==================== Workout Media Schemas ====================

class WorkoutMediaBase(BaseModel):
    media_type: MediaType
    blob_url: str
    thumbnail_url: Optional[str] = None
    file_size_bytes: Optional[int] = Field(None, ge=0)

class WorkoutMediaCreate(WorkoutMediaBase):
    workout_id: int

class WorkoutMediaResponse(WorkoutMediaBase):
    id: int
    workout_id: int
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

class WorkoutWithExercisesResponse(WorkoutResponse):
    strength_exercises: List[StrengthExerciseResponse] = []
    cardio_activities: List[CardioActivityResponse] = []
    media: List[WorkoutMediaResponse] = []

# ==================== Composite/Nested Schemas ====================

class WorkoutWithExercisesResponse(WorkoutResponse):
    strength_exercises: List[StrengthExerciseResponse] = []
    cardio_activities: List[CardioActivityResponse] = []
    media: List[WorkoutMediaResponse] = []
    