from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.auth.tenant import Tenant
from app.core.permissions import admin_only
from app.core.auth import get_current_admin
from app.schemas.user import UserResponse
from app.models.auth.user import User

router = APIRouter(
    prefix="/v1/admin",
    tags=["Admin"],
    dependencies=[Depends(admin_only)]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tenants")
def list_tenants(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)  # 🔥 REQUIRED
):
    return db.query(Tenant).all()

@router.post("/tenants")
def create_tenant(name: str, type: str, db: Session = Depends(get_db)):
    tenant = Tenant(name=name, type=type)
    db.add(tenant)
    db.commit()
    return {"message": "Tenant created"}

@router.delete("/tenants/{tenant_id}")
def delete_tenant(tenant_id: str, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    db.delete(tenant)
    db.commit()
    return {"message": "Tenant deleted"}

@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    return db.query(User).all()

@router.delete("/users/{email}", status_code=200)
def delete_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 🔐 Safety check: prevent admin deleting themselves
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot delete themselves"
        )

    db.delete(user)
    db.commit()

    return {
        "message": f"User with email '{email}' deleted successfully"
    }
