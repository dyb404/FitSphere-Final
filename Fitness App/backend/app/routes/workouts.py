from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.models import Workout, User, Assignment
from app.schemas.schemas import WorkoutCreate, WorkoutUpdate, WorkoutResponse
from app.core.simple_auth import get_user_by_id

router = APIRouter(prefix="/api/workouts", tags=["workouts"])

@router.get("", response_model=List[WorkoutResponse])
def get_workouts(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # If user_id provided, filter by user role
    if user_id:
        user = get_user_by_id(user_id, db)
        if user.role == "trainer" or user.role == "admin":
            workouts = db.query(Workout).filter(Workout.trainer_id == user.id).all()
        else:
            # Clients see assigned workouts
            assignments = db.query(Assignment).filter(Assignment.client_id == user.id).all()
            workout_ids = [a.workout_id for a in assignments] if assignments else []
            if workout_ids:
                workouts = db.query(Workout).filter(Workout.id.in_(workout_ids)).all()
            else:
                workouts = []
    else:
        # No user_id - return all workouts
        workouts = db.query(Workout).all()
    
    # Add trainer name to each workout
    result = []
    for workout in workouts:
        trainer = db.query(User).filter(User.id == workout.trainer_id).first()
        workout_dict = {
            "id": workout.id,
            "trainer_id": workout.trainer_id,
            "title": workout.title,
            "description": workout.description,
            "trainer_name": trainer.name if trainer else None
        }
        result.append(workout_dict)
    
    return result

@router.post("", status_code=status.HTTP_201_CREATED, response_model=WorkoutResponse)
def create_workout(
    workout_data: WorkoutCreate,
    trainer_id: int = Query(..., description="Trainer ID"),
    db: Session = Depends(get_db)
):
    # Verify trainer exists
    trainer = get_user_by_id(trainer_id, db)
    if trainer.role != "trainer" and trainer.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only trainers can create workouts"
        )
    
    new_workout = Workout(
        trainer_id=trainer_id,
        title=workout_data.title,
        description=workout_data.description
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    
    return {
        "id": new_workout.id,
        "trainer_id": new_workout.trainer_id,
        "title": new_workout.title,
        "description": new_workout.description,
        "trainer_name": trainer.name
    }

@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout_by_id(
    workout_id: int,
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    trainer = db.query(User).filter(User.id == workout.trainer_id).first()
    return {
        "id": workout.id,
        "trainer_id": workout.trainer_id,
        "title": workout.title,
        "description": workout.description,
        "trainer_name": trainer.name if trainer else None
    }

@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: int,
    workout_data: WorkoutUpdate,
    trainer_id: int = Query(..., description="Trainer ID"),
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    trainer = get_user_by_id(trainer_id, db)
    if workout.trainer_id != trainer_id and trainer.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this workout"
        )
    
    if workout_data.title is not None:
        workout.title = workout_data.title
    if workout_data.description is not None:
        workout.description = workout_data.description
    
    db.commit()
    db.refresh(workout)
    
    return {
        "id": workout.id,
        "trainer_id": workout.trainer_id,
        "title": workout.title,
        "description": workout.description,
        "trainer_name": trainer.name
    }

@router.delete("/{workout_id}", status_code=status.HTTP_200_OK)
def delete_workout(
    workout_id: int,
    trainer_id: int = Query(..., description="Trainer ID"),
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    trainer = get_user_by_id(trainer_id, db)
    if workout.trainer_id != trainer_id and trainer.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this workout"
        )
    
    db.delete(workout)
    db.commit()
    
    return {"message": "Workout deleted successfully"}

