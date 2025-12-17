from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.models import HealthTip
from app.schemas.schemas import HealthTipCreate, HealthTipResponse
from app.core.security import get_current_admin

router = APIRouter(prefix="/api/health-tips", tags=["health-tips"])

@router.get("", response_model=List[HealthTipResponse])
def get_health_tips(db: Session = Depends(get_db)):
    tips = db.query(HealthTip).all()
    return tips

@router.post("", status_code=status.HTTP_201_CREATED, response_model=HealthTipResponse)
def create_health_tip(
    tip_data: HealthTipCreate,
    current_user = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    new_tip = HealthTip(
        title=tip_data.title,
        content=tip_data.content
    )
    db.add(new_tip)
    db.commit()
    db.refresh(new_tip)
    return new_tip

@router.get("/{tip_id}", response_model=HealthTipResponse)
def get_health_tip_by_id(tip_id: int, db: Session = Depends(get_db)):
    tip = db.query(HealthTip).filter(HealthTip.id == tip_id).first()
    if not tip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health tip not found"
        )
    return tip

