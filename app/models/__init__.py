# File: app/models/__init__.py

"""
Central import location for all SQLAlchemy models.
This ensures all models are imported in the correct order and available for:
- Alembic migrations
- Database initialization
- API routes
"""

# Import Base first (if you have a separate base.py in models)
# from app.db.session import Base

# ==================== Tenant Models ====================
from app.models.auth.tenant import Tenant
from app.models.auth.tenant_configs import TenantConfigs

# ==================== User Models ====================
from app.models.auth.user import User
from app.models.auth.user_profile import UserProfile
from app.models.auth.user_consent import UserConsent
from app.models.auth.notification_preferences import NotificationPreference

# ==================== Workout Models ====================
from app.models.workout_management.workout import Workout
from app.models.workout_management.strength_exercise import StrengthExercise
from app.models.workout_management.cardio_activity import CardioActivity
from app.models.workout_management.workout_media import WorkoutMedia

# ==================== Template Models ====================
from app.models.workout_management.workout_template import WorkoutTemplate
from app.models.workout_management.template_exercise import TemplateExercise

# ==================== Goal Models ====================
from app.models.goals.goal import Goal
from app.models.goals.goal_milestone import GoalMilestone

# ==================== Measurement Models ====================
from app.models.goals.body_measurement import BodyMeasurement
from app.models.goals.personal_record import PersonalRecord

# ==================== Audit Models ====================
from app.models.audit.audit_log import AuditLog

# ==================== Export All Models ====================
__all__ = [
    # Tenant
    "Tenant",
    "TenantConfigs",
    
    # User
    "User",
    "UserProfile",
    "UserConsent",
    "NotificationPreference",
    
    # Workout
    "Workout",
    "StrengthExercise",
    "CardioActivity",
    "WorkoutMedia",
    
    # Template
    "WorkoutTemplate",
    "TemplateExercise",
    
    # Goal
    "Goal",
    "GoalMilestone",
    
    # Measurement
    "BodyMeasurement",
    "PersonalRecord",
    
    # Audit
    "AuditLog",
]
