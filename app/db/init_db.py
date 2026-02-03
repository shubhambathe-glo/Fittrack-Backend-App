# ==================== Initial Data Seed Script ====================
# File: app/db/init_db.py

"""
Initialize database with default tenants
Run this once after database creation
"""

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models import Tenant


def init_db():
    """
    Create all tables and seed initial data
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if tenants already exist
        existing_tenants = db.query(Tenant).count()
        
        if existing_tenants == 0:
            # Seed default tenants
            tenants = [
                {"name": "Individuals", "type": "Public"},
                {"name": "Gold's Gym Pune", "type": "Gym"},
                {"name": "Infosys Wellness", "type": "Corporate"},
                {"name": "IIT Fitness Program", "type": "University"},
            ]
            
            for tenant_data in tenants:
                tenant = Tenant(**tenant_data)
                db.add(tenant)
            
            db.commit()
            print("✅ Database initialized with default tenants")
        else:
            print("ℹ️  Database already has tenants, skipping seed")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    