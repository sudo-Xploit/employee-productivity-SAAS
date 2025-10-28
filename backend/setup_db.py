#!/usr/bin/env python
"""
Database setup script for Employee Productivity API.
This script initializes the database and creates necessary tables.
"""

import os
import sys
from sqlalchemy import text

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base_class import Base
from app.db.session import engine, SessionLocal
from app.core.config import settings
from app.models import user, department, employee, project, timesheet


def init_db():
    """Initialize the database and create tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
    
    # Test the connection
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result:
            print("Database connection test successful.")
        else:
            print("Database connection test failed.")
    except Exception as e:
        print(f"Error testing database connection: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print(f"Using database URL: {settings.DATABASE_URL}")
    init_db()
    print("Database setup complete.")
