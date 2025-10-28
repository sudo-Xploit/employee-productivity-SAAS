from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.models.project import Project


def get(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()


def get_by_department(
    db: Session, *, department_id: int, skip: int = 0, limit: int = 100
) -> List[Project]:
    return db.query(Project).filter(Project.department_id == department_id).offset(skip).limit(limit).all()


def create(db: Session, *, obj_in: Dict[str, Any]) -> Project:
    db_obj = Project(
        name=obj_in.get("name"),
        department_id=obj_in.get("department_id"),
        cost=obj_in.get("cost"),
        revenue=obj_in.get("revenue"),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Project, obj_in: Dict[str, Any]
) -> Project:
    update_data = obj_in
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, *, project_id: int) -> Project:
    obj = db.query(Project).get(project_id)
    db.delete(obj)
    db.commit()
    return obj
