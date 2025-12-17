from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.models import Assignment, User, Workout
from app.schemas.schemas import AssignmentCreate, AssignmentResponse
from app.core.simple_auth import get_user_by_id

router = APIRouter(prefix="/api/assignments", tags=["assignments"])

@router.get("", response_model=List[AssignmentResponse])
def get_assignments(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # If user_id provided, filter by user role
    if user_id:
        user = get_user_by_id(user_id, db)
        if user.role == "trainer" or user.role == "admin":
            assignments = db.query(Assignment).all()
        else:
            assignments = db.query(Assignment).filter(Assignment.client_id == user_id).all()
    else:
        # No user_id - return all assignments
        assignments = db.query(Assignment).all()
    
    result = []
    for assignment in assignments:
        client = db.query(User).filter(User.id == assignment.client_id).first()
        workout = db.query(Workout).filter(Workout.id == assignment.workout_id).first()
        result.append({
            "id": assignment.id,
            "client_id": assignment.client_id,
            "workout_id": assignment.workout_id,
            "client_name": client.name if client else None,
            "workout_title": workout.title if workout else None
        })
    
    return result

@router.post("", status_code=status.HTTP_201_CREATED, response_model=AssignmentResponse)
def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db)
):
    # Check if client exists
    client = get_user_by_id(assignment_data.client_id, db)
    if client.role != "client":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a client"
        )
    
    # Check if workout exists
    workout = db.query(Workout).filter(Workout.id == assignment_data.workout_id).first()
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    # Check if assignment already exists
    existing = db.query(Assignment).filter(
        Assignment.client_id == assignment_data.client_id,
        Assignment.workout_id == assignment_data.workout_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Workout already assigned to this client"
        )
    
    new_assignment = Assignment(
        client_id=assignment_data.client_id,
        workout_id=assignment_data.workout_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return {
        "id": new_assignment.id,
        "client_id": new_assignment.client_id,
        "workout_id": new_assignment.workout_id,
        "client_name": client.name,
        "workout_title": workout.title
    }

@router.delete("/{assignment_id}", status_code=status.HTTP_200_OK)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    db.delete(assignment)
    db.commit()
    
    return {"message": "Assignment removed successfully"}

