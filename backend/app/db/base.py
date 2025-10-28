# Import all the models, so that Base has them before being imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.department import Department  # noqa
from app.models.employee import Employee  # noqa
from app.models.project import Project  # noqa
from app.models.timesheet import Timesheet  # noqa