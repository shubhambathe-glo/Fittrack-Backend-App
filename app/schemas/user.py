from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from app.schemas.enums import Gender, UnitPreference, ConsentType
from app.schemas.notification import NotificationPreferenceResponse

# ==================== User Schemas ====================

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    tenant_id: int
    is_admin: bool = False

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_admin: bool
    tenant_id: int
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ==================== User Profile Schemas ====================

class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    height_cm: Optional[float] = Field(None, gt=0, le=300)
    unit_preference: UnitPreference = UnitPreference.METRIC
    timezone: str = "UTC"
    language: str = "en"
    preferences: Optional[Dict[str, Any]] = None

class UserProfileCreate(UserProfileBase):
    user_id: int

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

# ==================== User Consent Schemas ====================

class UserConsentBase(BaseModel):
    consent_type: ConsentType
    granted: bool
    version: str

class UserConsentCreate(UserConsentBase):
    user_id: int

class UserConsentUpdate(BaseModel):
    granted: bool

class UserConsentResponse(UserConsentBase):
    id: int
    user_id: int
    granted_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None

    # ✅ Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

# ==================== Composite/Nested Schemas ====================

class UserDetailResponse(UserResponse):
    profile: Optional[UserProfileResponse] = None
    notification_preference: Optional[NotificationPreferenceResponse] = None
