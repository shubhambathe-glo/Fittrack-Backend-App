from app.db.session import SessionLocal
from app.models.auth.tenant import Tenant

TENANTS = [
    {"name": "Individuals", "type": "Public"},
    {"name": "Gold’s Gym Pune", "type": "Gym"},
    {"name": "Infosys Wellness", "type": "Corporate"},
    {"name": "IIT Fitness Program", "type": "University"},
]

def seed_tenants():
    db = SessionLocal()

    for t in TENANTS:
        exists = db.query(Tenant).filter(Tenant.name == t["name"]).first()
        if not exists:
            db.add(Tenant(**t))

    db.commit()
    db.close()
