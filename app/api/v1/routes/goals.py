# ==================== Goal Routes ====================
# File: app/api/v1/routes/goals.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from typing import Optional
from app.db.session import get_db
from app.api.deps import get_current_user, PaginationParams
from app.schemas import (
    GoalCreate, GoalUpdate, GoalResponse, GoalWithMilestonesResponse,
    GoalMilestoneCreate, GoalMilestoneResponse
)
from app.models import User, Goal, GoalMilestone
from app.api.responses import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post("", response_model=ResponseModel[GoalResponse])
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new goal
    """
    if goal_data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create goal for other users")
    
    goal = Goal(**goal_data.dict())
    db.add(goal)
    db.commit()
    db.refresh(goal)

    from app.schemas import GoalResponse
    goal_response = GoalResponse.model_validate(goal)
    
    return ResponseModel(
        success=True,
        data=goal_response,
        message="Goal created successfully"
    )


@router.get("", response_model=PaginatedResponse[GoalResponse])
async def list_goals(
    pagination: PaginationParams = Depends(),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Goal).filter(Goal.user_id == current_user.id)

    if status:
        query = query.filter(Goal.status == status)

    total_items = query.count()

    goals = (
        query.order_by(Goal.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.page_size)
        .all()
    )

    total_pages = (total_items + pagination.page_size - 1) // pagination.page_size

    return PaginatedResponse(
        success=True,
        data=[GoalResponse.model_validate(goal) for goal in goals],  # MUST be list
        message="Goals retrieved successfully",
        page=pagination.page,
        page_size=pagination.page_size,
        total_items=total_items,
        total_pages=total_pages
    )


@router.get("/{goal_id}", response_model=ResponseModel[GoalWithMilestonesResponse])
async def get_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get goal with milestones
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    if goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return ResponseModel(
        success=True,
        data=goal,
        message="Goal retrieved successfully"
    )


@router.put("/{goal_id}", response_model=ResponseModel[GoalResponse])
async def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update goal
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    if goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    update_data = goal_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    db.commit()
    db.refresh(goal)
    
    return ResponseModel(
        success=True,
        data=goal,
        message="Goal updated successfully"
    )


@router.delete("/{goal_id}", response_model=ResponseModel[None])
async def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete goal
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    if goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(goal)
    db.commit()
    
    return ResponseModel(
        success=True,
        data=None,
        message="Goal deleted successfully"
    )


@router.post("/{goal_id}/milestones", response_model=ResponseModel[GoalMilestoneResponse])
async def add_milestone(
    goal_id: int,
    milestone_data: GoalMilestoneCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add milestone to goal
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    if goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    milestone = GoalMilestone(**milestone_data.dict())
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    
    return ResponseModel(
        success=True,
        data=milestone,
        message="Milestone added successfully"
    )
