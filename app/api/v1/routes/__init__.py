# ==================== Router Index File ====================
# File: app/api/v1/routes/__init__.py

"""
Export all routers for easy import
"""

from . import admin
from . import auth
from . import users
from . import workouts
from . import goals
from . import measurements
from . import tenants

__all__ = [
    "admin",
    "auth",
    "users", 
    "workouts",
    "goals",
    "measurements",
    "tenants"
]
