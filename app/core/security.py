# ==================== Security Utils ====================
# File: app/core/security.py

from datetime import datetime, timedelta, timezone
from jose import jwt
from argon2 import PasswordHasher
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False

def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==================== Additional Security Helpers ====================

from typing import Optional, Dict, Any
from jose import JWTError


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT access token
    
    Args:
        token: JWT token string
        
    Returns:
        dict: Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_token(token: str) -> Optional[int]:
    """
    Verify token and extract user_id
    
    Args:
        token: JWT token string
        
    Returns:
        int: User ID if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None


# ==================== Password Validation ====================

import re


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password: Plain text password
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


# ==================== Rate Limiting (Optional) ====================

from datetime import datetime
from typing import Dict
from fastapi import HTTPException, status


class RateLimiter:
    """
    Simple in-memory rate limiter for API endpoints
    For production, use Redis-based rate limiting
    """
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def check_rate_limit(self, identifier: str) -> bool:
        """
        Check if request is within rate limit
        
        Args:
            identifier: Unique identifier (e.g., user_id or IP address)
            
        Returns:
            bool: True if within limit, raises HTTPException otherwise
        """
        now = datetime.now(timezone.utc)
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests outside the time window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if (now - req_time).total_seconds() < self.window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[identifier]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {self.max_requests} requests per {self.window_seconds} seconds"
            )
        
        # Add current request
        self.requests[identifier].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


# ==================== Audit Logging Helper ====================

from typing import Optional, Any
from sqlalchemy.orm import Session
from app.models import AuditLog


def log_audit_event(
    db: Session,
    user_id: Optional[int],
    action_type: str,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    old_value: Optional[Dict[str, Any]] = None,
    new_value: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditLog:
    """
    Create audit log entry for security-critical actions
    
    Args:
        db: Database session
        user_id: ID of user performing action
        action_type: Type of action (login, create, update, delete, export)
        entity_type: Type of entity affected
        entity_id: ID of entity affected
        old_value: Previous value (for updates)
        new_value: New value (for creates/updates)
        ip_address: Client IP address
        user_agent: Client user agent string
        
    Returns:
        AuditLog: Created audit log entry
    """
    audit_log = AuditLog(
        user_id=user_id,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        old_value=old_value,
        new_value=new_value,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    
    return audit_log
