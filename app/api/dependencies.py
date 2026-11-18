from fastapi import Depends
from app.services.category import CategoryService
from app.services.task import TaskService
from app.db.session import get_db
from sqlalchemy.orm import Session


def get_task_service(db: Session = Depends(get_db)):
    return TaskService(db)


def get_category_service(db: Session = Depends(get_db)):
    return CategoryService(db)