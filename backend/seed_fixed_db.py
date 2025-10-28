import os
import sys
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.base import Base
from app.models.department import Department
from app.models.employee import Employee
from app.models.project import Project
from app.models.timesheet import Timesheet
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_db():
    """Seed the database with initial data."""
    db = SessionLocal()
    
    try:
        # Create admin user if it doesn't exist
        user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
        if not user:
            user = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                full_name="Administrator",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Admin user created")
        
        # Create sample departments if they don't exist
        if db.query(Department).count() == 0:
            departments = [
                Department(name="Engineering", budget=500000.0),
                Department(name="Marketing", budget=300000.0),
                Department(name="Sales", budget=400000.0),
                Department(name="Human Resources", budget=200000.0),
                Department(name="Finance", budget=250000.0),
            ]
            db.add_all(departments)
            db.commit()
            for dept in departments:
                db.refresh(dept)
            print("Sample departments created")
        else:
            departments = db.query(Department).all()
        
        # Create sample employees if they don't exist
        if db.query(Employee).count() == 0:
            employees = [
                # Engineering
                Employee(name="John Smith", department_id=1, salary=120000.0, revenue_generated=250000.0),
                Employee(name="Jane Doe", department_id=1, salary=110000.0, revenue_generated=220000.0),
                Employee(name="Mike Johnson", department_id=1, salary=95000.0, revenue_generated=180000.0),
                
                # Marketing
                Employee(name="Sarah Williams", department_id=2, salary=90000.0, revenue_generated=200000.0),
                Employee(name="David Brown", department_id=2, salary=85000.0, revenue_generated=170000.0),
                
                # Sales
                Employee(name="Emily Davis", department_id=3, salary=100000.0, revenue_generated=300000.0),
                Employee(name="Robert Wilson", department_id=3, salary=95000.0, revenue_generated=280000.0),
                Employee(name="Jennifer Taylor", department_id=3, salary=90000.0, revenue_generated=260000.0),
                
                # HR
                Employee(name="Michael Anderson", department_id=4, salary=85000.0, revenue_generated=100000.0),
                Employee(name="Lisa Thomas", department_id=4, salary=80000.0, revenue_generated=90000.0),
                
                # Finance
                Employee(name="James Martinez", department_id=5, salary=110000.0, revenue_generated=150000.0),
                Employee(name="Patricia Robinson", department_id=5, salary=100000.0, revenue_generated=130000.0),
            ]
            db.add_all(employees)
            db.commit()
            for emp in employees:
                db.refresh(emp)
            print("Sample employees created")
        
        # Create sample projects if they don't exist
        if db.query(Project).count() == 0:
            projects = [
                # Engineering
                Project(name="Product Redesign", department_id=1, cost=50000.0, revenue=150000.0),
                Project(name="Mobile App Development", department_id=1, cost=80000.0, revenue=200000.0),
                
                # Marketing
                Project(name="Brand Campaign", department_id=2, cost=40000.0, revenue=120000.0),
                Project(name="Social Media Strategy", department_id=2, cost=25000.0, revenue=80000.0),
                
                # Sales
                Project(name="Enterprise Client Acquisition", department_id=3, cost=30000.0, revenue=200000.0),
                Project(name="Sales Team Training", department_id=3, cost=15000.0, revenue=50000.0),
                
                # HR
                Project(name="Employee Wellness Program", department_id=4, cost=20000.0, revenue=40000.0),
                
                # Finance
                Project(name="Cost Optimization", department_id=5, cost=10000.0, revenue=100000.0),
            ]
            db.add_all(projects)
            db.commit()
            for proj in projects:
                db.refresh(proj)
            print("Sample projects created")
        
        # Create sample timesheets if they don't exist
        if db.query(Timesheet).count() == 0:
            timesheets = [
                # Engineering employees on engineering projects
                Timesheet(employee_id=1, project_id=1, hours_worked=40.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=1, project_id=2, hours_worked=40.0, date=date(2023, 10, 8)),
                Timesheet(employee_id=2, project_id=1, hours_worked=35.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=2, project_id=2, hours_worked=45.0, date=date(2023, 10, 8)),
                Timesheet(employee_id=3, project_id=1, hours_worked=38.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=3, project_id=2, hours_worked=42.0, date=date(2023, 10, 8)),
                
                # Marketing employees on marketing projects
                Timesheet(employee_id=4, project_id=3, hours_worked=40.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=4, project_id=4, hours_worked=40.0, date=date(2023, 10, 8)),
                Timesheet(employee_id=5, project_id=3, hours_worked=38.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=5, project_id=4, hours_worked=42.0, date=date(2023, 10, 8)),
                
                # Sales employees on sales projects
                Timesheet(employee_id=6, project_id=5, hours_worked=45.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=6, project_id=6, hours_worked=40.0, date=date(2023, 10, 8)),
                Timesheet(employee_id=7, project_id=5, hours_worked=40.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=7, project_id=6, hours_worked=40.0, date=date(2023, 10, 8)),
                Timesheet(employee_id=8, project_id=5, hours_worked=38.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=8, project_id=6, hours_worked=42.0, date=date(2023, 10, 8)),
                
                # HR employees on HR projects
                Timesheet(employee_id=9, project_id=7, hours_worked=40.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=9, project_id=7, hours_worked=40.0, date=date(2023, 10, 8)),
                Timesheet(employee_id=10, project_id=7, hours_worked=38.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=10, project_id=7, hours_worked=42.0, date=date(2023, 10, 8)),
                
                # Finance employees on finance projects
                Timesheet(employee_id=11, project_id=8, hours_worked=40.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=11, project_id=8, hours_worked=40.0, date=date(2023, 10, 8)),
                Timesheet(employee_id=12, project_id=8, hours_worked=38.0, date=date(2023, 10, 1)),
                Timesheet(employee_id=12, project_id=8, hours_worked=42.0, date=date(2023, 10, 8)),
            ]
            db.add_all(timesheets)
            db.commit()
            print(f"Created {len(timesheets)} sample timesheets")
        
        print("Database seeding completed")
    
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
