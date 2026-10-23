from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import Interview, JobApplication, User
from app.schemas import InterviewCreate, InterviewResponse

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(JobApplication).filter(JobApplication.id == interview.application_id, JobApplication.user_id == current_user.id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    new_interview = Interview(application_id=interview.application_id, interview_date=interview.interview_date, interview_type=interview.interview_type, notes=interview.notes)
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return new_interview

@router.get("", response_model=list[InterviewResponse])
def get_interviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Interview).join(JobApplication).filter(JobApplication.user_id == current_user.id).order_by(Interview.interview_date).all()

@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(interview_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    interview = db.query(Interview).join(JobApplication).filter(Interview.id == interview_id, JobApplication.user_id == current_user.id).first()
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview
