from sqlalchemy.orm import Session
from models import Task
from datetime import datetime

def create_task(db: Session, user_id: int, title: str, description: str = "", deadline: datetime = None, subject: str = ""):
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        deadline=deadline,
        subject=subject,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

def mark_task_completed(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = "completed"
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
