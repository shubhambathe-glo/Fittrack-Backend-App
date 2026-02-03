# ==================== Workout Routes ====================
# File: app/api/v1/routes/workouts.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.db.session import get_db
from app.api.deps import get_current_user, PaginationParams
from app.schemas.workout import (
    WorkoutCreate, WorkoutUpdate, WorkoutResponse, WorkoutWithExercisesResponse,
    StrengthExerciseCreate, StrengthExerciseResponse,
    CardioActivityCreate, CardioActivityResponse
)
from app.models import User, Workout, StrengthExercise, CardioActivity
from app.api.responses import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post("", response_model=ResponseModel[WorkoutResponse])
async def create_workout(
    workout_data: WorkoutCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new workout
    """
    # Tenant isolation: Ensure workout is created for current user
    if workout_data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create workout for other users")
    
    workout = Workout(**workout_data.dict())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    
    return ResponseModel(
        success=True,
        data=workout,
        message="Workout created successfully"
    )


@router.get("", response_model=PaginatedResponse[WorkoutResponse])
async def list_workouts(
    pagination: PaginationParams = Depends(),
    workout_type: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's workouts with filters and pagination
    """
    query = db.query(Workout).filter(Workout.user_id == current_user.id)
    
    # Apply filters
    if workout_type:
        query = query.filter(Workout.workout_type == workout_type)
    if from_date:
        query = query.filter(Workout.workout_datetime >= from_date)
    if to_date:
        query = query.filter(Workout.workout_datetime <= to_date)
    
    # Get total count
    total_items = query.count()
    
    # Apply pagination
    workouts = query.order_by(Workout.workout_datetime.desc())\
        .offset(pagination.skip)\
        .limit(pagination.page_size)\
        .all()
    
    total_pages = (total_items + pagination.page_size - 1) // pagination.page_size
    
    return PaginatedResponse(
        success=True,
        data=workouts,
        message="Workouts retrieved successfully",
        page=pagination.page,
        page_size=pagination.page_size,
        total_items=total_items,
        total_pages=total_pages
    )


@router.get("/{workout_id}", response_model=ResponseModel[WorkoutWithExercisesResponse])
async def get_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get workout details with exercises
    """
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Tenant isolation check
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return ResponseModel(
        success=True,
        data=workout,
        message="Workout retrieved successfully"
    )


@router.put("/{workout_id}", response_model=ResponseModel[WorkoutResponse])
async def update_workout(
    workout_id: int,
    workout_data: WorkoutUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update workout
    """
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Tenant isolation check
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    update_data = workout_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workout, field, value)
    
    db.commit()
    db.refresh(workout)
    
    return ResponseModel(
        success=True,
        data=workout,
        message="Workout updated successfully"
    )


@router.delete("/{workout_id}", response_model=ResponseModel[None])
async def delete_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete workout
    """
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Tenant isolation check
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(workout)
    db.commit()
    
    return ResponseModel(
        success=True,
        data=None,
        message="Workout deleted successfully"
    )


@router.post("/{workout_id}/strength-exercises", response_model=ResponseModel[StrengthExerciseResponse])
async def add_strength_exercise(
    workout_id: int,
    exercise_data: StrengthExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add strength exercise to workout
    """
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Tenant isolation check
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    exercise = StrengthExercise(**exercise_data.dict())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    
    return ResponseModel(
        success=True,
        data=exercise,
        message="Strength exercise added successfully"
    )


@router.post("/{workout_id}/cardio-activities", response_model=ResponseModel[CardioActivityResponse])
async def add_cardio_activity(
    workout_id: int,
    activity_data: CardioActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add cardio activity to workout
    """
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # Tenant isolation check
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    activity = CardioActivity(**activity_data.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return ResponseModel(
        success=True,
        data=activity,
        message="Cardio activity added successfully"
    )
