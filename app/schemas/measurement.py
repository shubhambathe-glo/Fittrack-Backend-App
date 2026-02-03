from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# ==================== Body Measurement Schemas ====================

class BodyMeasurementBase(BaseModel):
    metric_type: str
    value: float
    unit: str
    measured_at: datetime
    notes: Optional[str] = None


class BodyMeasurementCreate(BodyMeasurementBase):
    user_id: int


class BodyMeasurementUpdate(BaseModel):
    value: Optional[float] = None
    notes: Optional[str] = None


class BodyMeasurementResponse(BodyMeasurementBase):
    id: int
    user_id: int
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)


# ==================== Personal Record Schemas ====================

class PersonalRecordBase(BaseModel):
    exercise_name: str
    record_type: str
    value: float
    unit: str
    workout_id: Optional[int] = None
    achieved_at: datetime


class PersonalRecordCreate(PersonalRecordBase):
    user_id: int


class PersonalRecordResponse(PersonalRecordBase):
    id: int
    user_id: int
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)
