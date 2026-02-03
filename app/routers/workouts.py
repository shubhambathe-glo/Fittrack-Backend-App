from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.workout_management.workout import Workout
from app.schemas.workout import WorkoutCreate
from app.core.auth import get_current_user

router = APIRouter(prefix="/v1/workouts", tags=["Workouts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_workout(
    workout: WorkoutCreate,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_workout = Workout(
        **workout.dict(),
        user_id=current["user_id"],
        tenant_id=current["tenant_id"]
    )
    db.add(db_workout)
    db.commit()
    return {
        "workoutId": db_workout.id,
        "status": "created"
    }

@router.get("/")
def list_workouts(userId: str, db: Session = Depends(get_db)):
    return db.query(Workout).filter(Workout.user_id == userId).all()
