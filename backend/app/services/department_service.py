from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.models.department import Department


def get(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()


def get_by_name(db: Session, name: str) -> Optional[Department]:
    return db.query(Department).filter(Department.name == name).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Department]:
    return db.query(Department).offset(skip).limit(limit).all()


def create(db: Session, *, obj_in: Dict[str, Any]) -> Department:
    db_obj = Department(
        name=obj_in.get("name"),
        budget=obj_in.get("budget"),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Department, obj_in: Dict[str, Any]
) -> Department:
    update_data = obj_in
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, *, department_id: int) -> Department:
    obj = db.query(Department).get(department_id)
    db.delete(obj)
    db.commit()
    return obj
