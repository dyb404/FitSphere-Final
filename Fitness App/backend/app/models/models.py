from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, trainer, client
    
    # Relationships
    workouts = relationship("Workout", back_populates="trainer", cascade="all, delete-orphan")
    assignments_as_client = relationship("Assignment", foreign_keys="Assignment.client_id", back_populates="client", cascade="all, delete-orphan")
    progress_logs = relationship("ProgressLog", back_populates="client", cascade="all, delete-orphan")

class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    trainer = relationship("User", back_populates="workouts")
    assignments = relationship("Assignment", back_populates="workout", cascade="all, delete-orphan")

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    
    __table_args__ = (UniqueConstraint('client_id', 'workout_id', name='unique_client_workout'),)
    
    # Relationships
    client = relationship("User", foreign_keys=[client_id], back_populates="assignments_as_client")
    workout = relationship("Workout", back_populates="assignments")

class ProgressLog(Base):
    __tablename__ = "progress_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    weight = Column(Float, nullable=True)
    calories = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    client = relationship("User", back_populates="progress_logs")

class HealthTip(Base):
    __tablename__ = "health_tips"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

