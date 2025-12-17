from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/clients", response_model=List[UserResponse])
def get_all_clients(db: Session = Depends(get_db)):
    clients = db.query(User).filter(User.role == "client").all()
    return clients

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

