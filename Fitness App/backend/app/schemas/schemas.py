from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime

# User Schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Optional[str] = "client"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Workout Schemas
class WorkoutCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

class WorkoutUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None

class WorkoutResponse(BaseModel):
    id: int
    trainer_id: int
    title: str
    description: Optional[str]
    trainer_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# Assignment Schemas
class AssignmentCreate(BaseModel):
    client_id: int
    workout_id: int

class AssignmentResponse(BaseModel):
    id: int
    client_id: int
    workout_id: int
    client_name: Optional[str] = None
    workout_title: Optional[str] = None
    
    class Config:
        from_attributes = True

# Progress Log Schemas
class ProgressLogCreate(BaseModel):
    date: date
    weight: Optional[float] = None
    calories: Optional[int] = None
    notes: Optional[str] = None

class ProgressLogResponse(BaseModel):
    id: int
    client_id: int
    date: date
    weight: Optional[float]
    calories: Optional[int]
    notes: Optional[str]
    
    class Config:
        from_attributes = True

# Health Tip Schemas
class HealthTipCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

class HealthTipResponse(BaseModel):
    id: int
    title: str
    content: str
    
    class Config:
        from_attributes = True

