from fastapi import Depends, HTTPException, status
from app.core.auth import get_current_user
from app.models.auth.user import User

def admin_only(current: User = Depends(get_current_user)):
    if not current.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current
