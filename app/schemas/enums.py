from enum import Enum

class UserType(str, Enum):
    USER = "user"
    ADMIN = "admin"

class TenantType(str, Enum):
    PUBLIC = "Public"
    GYM = "Gym"
    CORPORATE = "Corporate"
    UNIVERSITY = "University"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"

class UnitPreference(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"

class WorkoutType(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    MIXED = "mixed"

class WorkoutStatus(str, Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class ConsentType(str, Enum):
    DATA_PROCESSING = "data_processing"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    THIRD_PARTY_SHARING = "third_party_sharing"

class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
