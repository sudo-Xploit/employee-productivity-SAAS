from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.models.employee import Employee


def get(db: Session, employee_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()


def get_by_department(
    db: Session, *, department_id: int, skip: int = 0, limit: int = 100
) -> List[Employee]:
    return db.query(Employee).filter(Employee.department_id == department_id).offset(skip).limit(limit).all()


def create(db: Session, *, obj_in: Dict[str, Any]) -> Employee:
    db_obj = Employee(
        name=obj_in.get("name"),
        department_id=obj_in.get("department_id"),
        salary=obj_in.get("salary"),
        revenue_generated=obj_in.get("revenue_generated", 0.0),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Employee, obj_in: Dict[str, Any]
) -> Employee:
    update_data = obj_in
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, *, employee_id: int) -> Employee:
    obj = db.query(Employee).get(employee_id)
    db.delete(obj)
    db.commit()
    return obj
