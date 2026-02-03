from app.db.session import SessionLocal
from app.models.auth.user import User
from app.models.auth.tenant import Tenant
from app.core.security import hash_password

def seed_admin():
    db = SessionLocal()

    # Check if admin already exists
    if db.query(User).filter(User.is_admin == True).first():
        db.close()
        return

    # Get ANY tenant (now guaranteed to exist)
    tenant = db.query(Tenant).first()
    if not tenant:
        raise RuntimeError("No tenants found. Seed tenants first.")

    admin = User(
        email="admin@fitnessapp.com",
        hashed_password=hash_password("Admin@123"),
        is_admin=True,
        tenant_id=tenant.id
    )

    db.add(admin)
    db.commit()
    db.close()
