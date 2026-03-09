from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student") # "student" or "teacher"
    session_token = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")
    academic_data = relationship("AcademicData", back_populates="user", uselist=False, cascade="all, delete-orphan")


class AcademicData(Base):
    __tablename__ = "academic_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Input metrics mapping to final_dataset
    attendance = Column(Float, default=75.0)
    hours_studied = Column(Float, default=15.0)
    sleep_hours = Column(Float, default=7.0)
    previous_scores = Column(Float, default=70.0)
    physical_activity = Column(Float, default=3.0)
    parental_involvement = Column(Float, default=2.0)
    internet_access = Column(Integer, default=1) # 1 for Yes, 0 for No
    
    # Computed risk metrics (can be cached here)
    risk_score = Column(Float, default=0.0)
    risk_category = Column(String, default="Low Risk")
    cluster = Column(Integer, default=0)

    user = relationship("User", back_populates="academic_data")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    deadline = Column(DateTime)
    subject = Column(String)
    status = Column(String, default="pending") # "pending" or "completed"
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tasks")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_name = Column(String, nullable=False)
    description = Column(String)
    icon_name = Column(String) # For streamlit icon rendering
    earned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="achievements")
