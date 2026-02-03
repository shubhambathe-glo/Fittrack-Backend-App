from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.goals.goal import Goal

router = APIRouter(prefix="/v1/goals", tags=["Goals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_goal(goal: dict, db: Session = Depends(get_db)):
    db_goal = Goal(**goal)
    db.add(db_goal)
    db.commit()
    return {"goalId": db_goal.id}
