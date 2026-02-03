# ==================== User Profile Routes ====================
# File: app/api/v1/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas import (
    UserProfileResponse, UserProfileUpdate, UserDetailResponse,
    NotificationPreferenceResponse, NotificationPreferenceUpdate,
    UserConsentCreate, UserConsentResponse
)
from app.models import User, UserProfile, NotificationPreference, UserConsent
from app.api.responses import ResponseModel

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=ResponseModel[UserDetailResponse])
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's complete profile
    """
    return ResponseModel(
        success=True,
        data=current_user,
        message="User profile retrieved successfully"
    )


@router.put("/me/profile", response_model=ResponseModel[UserProfileResponse])
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    """
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    return ResponseModel(
        success=True,
        data=profile,
        message="Profile updated successfully"
    )


@router.put("/me/notifications", response_model=ResponseModel[NotificationPreferenceResponse])
async def update_notification_preferences(
    notif_data: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update notification preferences
    """
    notif_pref = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id
    ).first()
    
    if not notif_pref:
        raise HTTPException(status_code=404, detail="Notification preferences not found")
    
    update_data = notif_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(notif_pref, field, value)
    
    db.commit()
    db.refresh(notif_pref)
    
    return ResponseModel(
        success=True,
        data=notif_pref,
        message="Notification preferences updated successfully"
    )


@router.post("/me/consents", response_model=ResponseModel[UserConsentResponse])
async def create_consent(
    consent_data: UserConsentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Record user consent (GDPR/CCPA compliance)
    """
    from datetime import datetime
    
    consent = UserConsent(
        user_id=current_user.id,
        consent_type=consent_data.consent_type,
        granted=consent_data.granted,
        version=consent_data.version,
        granted_at=datetime.utcnow() if consent_data.granted else None
    )
    
    db.add(consent)
    db.commit()
    db.refresh(consent)
    
    return ResponseModel(
        success=True,
        data=consent,
        message="Consent recorded successfully"
    )
