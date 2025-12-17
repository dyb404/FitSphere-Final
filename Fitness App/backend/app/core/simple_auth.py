"""
Simple authentication - no JWT tokens, just user lookup
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User

def get_user_by_id(user_id: int, db: Session) -> User:
    """Get user by ID - simple lookup, no token needed"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def get_user_by_email(email: str, db: Session) -> User:
    """Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

