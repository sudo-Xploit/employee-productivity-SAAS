import logging
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.department import Department
from app.models.employee import Employee
from app.models.project import Project
from app.models.timesheet import Timesheet
from app.models.user import User, UserRole
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """Initialize the database with sample data."""
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
        logger.info("Admin user created")
    
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
        logger.info("Sample departments created")
    else:
        departments = db.query(Department).all()
    
    # Create sample employees if they don't exist
    if db.query(Employee).count() == 0:
        employees = [
            # Engineering
            Employee(name="John Smith", department_id=departments[0].id, salary=120000.0, revenue_generated=250000.0),
            Employee(name="Jane Doe", department_id=departments[0].id, salary=110000.0, revenue_generated=220000.0),
            Employee(name="Mike Johnson", department_id=departments[0].id, salary=95000.0, revenue_generated=180000.0),
            
            # Marketing
            Employee(name="Sarah Williams", department_id=departments[1].id, salary=90000.0, revenue_generated=200000.0),
            Employee(name="David Brown", department_id=departments[1].id, salary=85000.0, revenue_generated=170000.0),
            
            # Sales
            Employee(name="Emily Davis", department_id=departments[2].id, salary=100000.0, revenue_generated=300000.0),
            Employee(name="Robert Wilson", department_id=departments[2].id, salary=95000.0, revenue_generated=280000.0),
            Employee(name="Jennifer Taylor", department_id=departments[2].id, salary=90000.0, revenue_generated=260000.0),
            
            # HR
            Employee(name="Michael Anderson", department_id=departments[3].id, salary=85000.0, revenue_generated=100000.0),
            Employee(name="Lisa Thomas", department_id=departments[3].id, salary=80000.0, revenue_generated=90000.0),
            
            # Finance
            Employee(name="James Martinez", department_id=departments[4].id, salary=110000.0, revenue_generated=150000.0),
            Employee(name="Patricia Robinson", department_id=departments[4].id, salary=100000.0, revenue_generated=130000.0),
        ]
        db.add_all(employees)
        db.commit()
        for emp in employees:
            db.refresh(emp)
        logger.info("Sample employees created")
    else:
        employees = db.query(Employee).all()
    
    # Create sample projects if they don't exist
    if db.query(Project).count() == 0:
        projects = [
            # Engineering
            Project(name="Product Redesign", department_id=departments[0].id, cost=50000.0, revenue=150000.0),
            Project(name="Mobile App Development", department_id=departments[0].id, cost=80000.0, revenue=200000.0),
            
            # Marketing
            Project(name="Brand Campaign", department_id=departments[1].id, cost=40000.0, revenue=120000.0),
            Project(name="Social Media Strategy", department_id=departments[1].id, cost=25000.0, revenue=80000.0),
            
            # Sales
            Project(name="Enterprise Client Acquisition", department_id=departments[2].id, cost=30000.0, revenue=200000.0),
            Project(name="Sales Team Training", department_id=departments[2].id, cost=15000.0, revenue=50000.0),
            
            # HR
            Project(name="Employee Wellness Program", department_id=departments[3].id, cost=20000.0, revenue=40000.0),
            
            # Finance
            Project(name="Cost Optimization", department_id=departments[4].id, cost=10000.0, revenue=100000.0),
        ]
        db.add_all(projects)
        db.commit()
        for proj in projects:
            db.refresh(proj)
        logger.info("Sample projects created")
    else:
        projects = db.query(Project).all()
    
    # Create sample timesheets if they don't exist
    if db.query(Timesheet).count() == 0:
        today = date.today()
        timesheets = []
        
        # Generate timesheets for the last 30 days
        for i in range(30):
            current_date = today - timedelta(days=i)
            
            # Skip weekends
            if current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                continue
            
            # For each employee, create timesheets for projects in their department
            for employee in employees:
                dept_projects = [p for p in projects if p.department_id == employee.department_id]
                if not dept_projects:
                    continue
                
                # Assign hours to projects
                for project in dept_projects:
                    # Random hours between 1 and 8
                    hours = 8.0 / len(dept_projects)
                    timesheets.append(
                        Timesheet(
                            employee_id=employee.id,
                            project_id=project.id,
                            hours_worked=hours,
                            date=current_date
                        )
                    )
        
        db.add_all(timesheets)
        db.commit()
        logger.info(f"Created {len(timesheets)} sample timesheets")
    
    logger.info("Database initialization completed")


def create_first_superuser(db: Session) -> None:
    """Create first superuser if it doesn't exist."""
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = {
            "email": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
            "full_name": "Initial Super User",
            "role": UserRole.ADMIN,
            "is_active": True,
        }
        user = User(
            email=user_in["email"],
            hashed_password=get_password_hash(user_in["password"]),
            full_name=user_in["full_name"],
            role=user_in["role"],
            is_active=user_in["is_active"],
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("Superuser created")
