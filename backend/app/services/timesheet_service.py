from datetime import date
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.models.timesheet import Timesheet


def get(db: Session, timesheet_id: int) -> Optional[Timesheet]:
    return db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Timesheet]:
    return db.query(Timesheet).offset(skip).limit(limit).all()


def get_by_employee(
    db: Session, *, employee_id: int, skip: int = 0, limit: int = 100
) -> List[Timesheet]:
    return db.query(Timesheet).filter(Timesheet.employee_id == employee_id).offset(skip).limit(limit).all()


def get_by_project(
    db: Session, *, project_id: int, skip: int = 0, limit: int = 100
) -> List[Timesheet]:
    return db.query(Timesheet).filter(Timesheet.project_id == project_id).offset(skip).limit(limit).all()


def get_by_date_range(
    db: Session, *, start_date: date, end_date: date, skip: int = 0, limit: int = 100
) -> List[Timesheet]:
    return db.query(Timesheet).filter(
        Timesheet.date >= start_date,
        Timesheet.date <= end_date
    ).offset(skip).limit(limit).all()


def create(db: Session, *, obj_in: Dict[str, Any]) -> Timesheet:
    db_obj = Timesheet(
        employee_id=obj_in.get("employee_id"),
        project_id=obj_in.get("project_id"),
        hours_worked=obj_in.get("hours_worked"),
        date=obj_in.get("date", date.today()),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Timesheet, obj_in: Dict[str, Any]
) -> Timesheet:
    update_data = obj_in
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, *, timesheet_id: int) -> Timesheet:
    obj = db.query(Timesheet).get(timesheet_id)
    db.delete(obj)
    db.commit()
    return obj
