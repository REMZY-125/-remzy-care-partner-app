"""
Create all database tables.
Run this whenever you add/change models.
"""

from app.database import Base, engine
from app import models  # noqa: F401 — imports all models


print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done. All tables created successfully.")