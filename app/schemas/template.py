from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.schemas import WorkoutType

# ==================== Workout Template Schemas ====================

class WorkoutTemplateBase(BaseModel):
    template_name: str
    workout_type: WorkoutType
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool = False

class WorkoutTemplateCreate(WorkoutTemplateBase):
    user_id: int

class WorkoutTemplateUpdate(BaseModel):
    template_name: Optional[str] = None
    workout_type: Optional[WorkoutType] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None

class WorkoutTemplateResponse(WorkoutTemplateBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

# ==================== Template Exercise Schemas ====================

class TemplateExerciseBase(BaseModel):
    exercise_name: str
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    order_index: int = 0
    notes: Optional[str] = None

class TemplateExerciseCreate(TemplateExerciseBase):
    template_id: int

class TemplateExerciseUpdate(BaseModel):
    exercise_name: Optional[str] = None
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    order_index: Optional[int] = None
    notes: Optional[str] = None

class TemplateExerciseResponse(TemplateExerciseBase):
    id: int
    template_id: int
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)
