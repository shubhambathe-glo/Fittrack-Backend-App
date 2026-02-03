from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, time

class NotificationPreferenceBase(BaseModel):
    email_enabled: bool = True
    push_enabled: bool = True
    workout_reminders: bool = True
    goal_milestones: bool = True
    streak_alerts: bool = True
    quiet_hours_start: Optional[time] = None
    quiet_hours_end: Optional[time] = None

class NotificationPreferenceCreate(NotificationPreferenceBase):
    user_id: int

class NotificationPreferenceUpdate(NotificationPreferenceBase):
    pass

class NotificationPreferenceResponse(NotificationPreferenceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)
