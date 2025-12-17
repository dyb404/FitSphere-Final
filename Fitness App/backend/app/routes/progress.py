from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.models import ProgressLog, User
from app.schemas.schemas import ProgressLogResponse
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProgressLogCreateWithClient(BaseModel):
    client_id: int
    date: date
    weight: Optional[float] = None
    calories: Optional[int] = None
    notes: Optional[str] = None
from app.core.simple_auth import get_user_by_id

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("", response_model=List[ProgressLogResponse])
def get_progress_logs(
    client_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Simple - filter by client_id if provided, otherwise return all
    if client_id:
        logs = db.query(ProgressLog).filter(ProgressLog.client_id == client_id).order_by(ProgressLog.date.desc()).all()
    else:
        logs = db.query(ProgressLog).order_by(ProgressLog.date.desc()).all()
    
    return logs

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProgressLogResponse)
def create_progress_log(
    log_data: ProgressLogCreateWithClient,
    db: Session = Depends(get_db)
):
    new_log = ProgressLog(
        client_id=log_data.client_id,
        date=log_data.date,
        weight=log_data.weight,
        calories=log_data.calories,
        notes=log_data.notes
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/{log_id}", response_model=ProgressLogResponse)
def get_progress_log_by_id(
    log_id: int,
    db: Session = Depends(get_db)
):
    log = db.query(ProgressLog).filter(ProgressLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress log not found"
        )
    return log

@router.delete("/{log_id}", status_code=status.HTTP_200_OK)
def delete_progress_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    log = db.query(ProgressLog).filter(ProgressLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress log not found"
        )
    
    db.delete(log)
    db.commit()
    
    return {"message": "Progress log deleted successfully"}

