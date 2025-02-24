from fastapi import FastAPI, HTTPException  # FastAPI framework imports
from pydantic import BaseModel  # Data validation
from datetime import datetime, timedelta  # Date/time handling
from celery import Celery  # Task queue for background processing
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis  # Redis for task scheduling

app = FastAPI()

# Database setup
DATABASE_URL = "postgresql://ndangu:Suaiubo_586799!@localhost/reminders_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis & Celery setup
REDIS_URL = "redis://localhost:6379/0"
celery = Celery("taskScheduler", broker=REDIS_URL, backend=REDIS_URL)

# Define Reminder model
class ReminderDB(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, unique=True, index=True)
    title = Column(String, index=True)
    due_date = Column(String)
    priority = Column(String)
    notify_time = Column(DateTime)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic model for request validation
class Reminder(BaseModel):
    task_id: int  # Unique identifier for task
    title: str  # Task title
    due_date: str  # YYYY-MM-DD format for task due date
    priority: str  # Task priority level
    notify_time: str  # ISO 8601 format for reminder time

# Celery task for sending notifications
@celery.task
def send_notification(task_id: int, title: str):
    print(f"[NOTIFICATION] Reminder for Task {task_id}: {title}")


@app.post("/api/reminders")
def schedule_reminder(reminder: Reminder):
    """Schedules a reminder for a task."""
    db = SessionLocal()
    notify_time = datetime.fromisoformat(reminder.notify_time)
    
    if notify_time < datetime.now():
        raise HTTPException(status_code=400, detail="Notification time must be in the future.")  # Ensure valid notify time
    
    new_reminder = ReminderDB(
        task_id=reminder.task_id,
        title=reminder.title,
        due_date=reminder.due_date,
        priority=reminder.priority,
        notify_time=notify_time
    )
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    db.close()
    
    delay = (notify_time - datetime.now()).total_seconds()
    send_notification.apply_async((reminder.task_id, reminder.title), countdown=delay)  # Queue notification task in Celery
    
    return {"status": "Reminder scheduled", "task_id": reminder.task_id}

@app.put("/api/reminders/{task_id}")
def update_reminder(task_id: int, reminder: Reminder):
    """Updates an existing reminder."""
    db = SessionLocal()
    db_reminder = db.query(ReminderDB).filter(ReminderDB.task_id == task_id).first()
    if not db_reminder:
        db.close()
        raise HTTPException(status_code=404, detail="Reminder not found.")
    
    db_reminder.title = reminder.title
    db_reminder.due_date = reminder.due_date
    db_reminder.priority = reminder.priority
    db_reminder.notify_time = datetime.fromisoformat(reminder.notify_time)
    db.commit()
    db.refresh(db_reminder)
    db.close()
    
    delay = (db_reminder.notify_time - datetime.now()).total_seconds()
    send_notification.apply_async((reminder.task_id, reminder.title), countdown=delay)  # Reschedule notification task
    
    return {"status": "Reminder updated", "task_id": task_id}

@app.delete("/api/reminders/{task_id}")
def cancel_reminder(task_id: int):
    """Cancels a scheduled reminder."""
    db = SessionLocal()
    db_reminder = db.query(ReminderDB).filter(ReminderDB.task_id == task_id).first()
    if not db_reminder:
        db.close()
        raise HTTPException(status_code=404, detail="Reminder not found.")
    
    db.delete(db_reminder)
    db.commit()
    db.close()
    
    return {"status": "Reminder canceled", "task_id": task_id}

@app.get("/api/reminders")
def get_reminders():
    """Returns all scheduled reminders."""
    db = SessionLocal()
    reminders = db.query(ReminderDB).all()
    db.close()
    return reminders 
