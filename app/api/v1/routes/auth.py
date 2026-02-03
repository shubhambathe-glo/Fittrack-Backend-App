# ==================== Auth Routes ====================
# File: app/api/v1/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.schemas import UserCreate, UserLogin, UserResponse
from app.models import User, Tenant, UserProfile, NotificationPreference
from app.core.security import hash_password, verify_password, create_access_token
from app.api.responses import ResponseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=ResponseModel[UserResponse])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if tenant exists
    tenant = db.query(Tenant).filter(Tenant.id == user_data.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Create user
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        tenant_id=user_data.tenant_id,
        is_admin=user_data.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create default user profile
    profile = UserProfile(user_id=new_user.id)
    db.add(profile)
    
    # Create default notification preferences
    notif_pref = NotificationPreference(user_id=new_user.id)
    db.add(notif_pref)
    
    db.commit()
    
    return ResponseModel(
        success=True,
        data=new_user,
        message="User registered successfully"
    )

@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login and get JWT token
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "tenant_id": user.tenant_id}
    )
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    
    return ResponseModel(
        success=True,
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        },
        message="Login successful"
    )
