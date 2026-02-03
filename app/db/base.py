# ==================== Database Base ====================
# File: app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models so SQLAlchemy registers them
import app.models  # noqa
