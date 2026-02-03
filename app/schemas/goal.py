from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from app.schemas.enums import GoalStatus

# ==================== Goal Schemas ====================

class GoalBase(BaseModel):
    goal_name: str
    metric_type: str
    target_value: float
    baseline_value: Optional[float] = None
    unit: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    status: GoalStatus = GoalStatus.ACTIVE


class GoalCreate(GoalBase):
    user_id: int


class GoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    metric_type: Optional[str] = None
    target_value: Optional[float] = None
    baseline_value: Optional[float] = None
    unit: Optional[str] = None
    end_date: Optional[date] = None
    status: Optional[GoalStatus] = None


class GoalResponse(GoalBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# ==================== Goal Milestone Schemas ====================

class GoalMilestoneBase(BaseModel):
    milestone_name: str
    milestone_value: float
    target_date: Optional[date] = None

class GoalMilestoneCreate(GoalMilestoneBase):
    goal_id: int

class GoalMilestoneUpdate(BaseModel):
    milestone_name: Optional[str] = None
    milestone_value: Optional[float] = None
    target_date: Optional[date] = None
    achieved: Optional[bool] = None

class GoalMilestoneResponse(GoalMilestoneBase):
    id: int
    goal_id: int
    achieved: bool
    achieved_at: Optional[datetime] = None
    created_at: datetime

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

# ==================== Composite/Nested Schemas ====================

class GoalWithMilestonesResponse(GoalResponse):
    milestones: List[GoalMilestoneResponse] = []
