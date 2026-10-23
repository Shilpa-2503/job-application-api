from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import JobApplication, User
from app.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["Job Applications"])

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_application = JobApplication(company=application.company, role=application.role, status=application.status, user_id=current_user.id)
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

@router.get("", response_model=list[ApplicationResponse])
def get_applications(status_filter: str | None = Query(default=None, alias="status"), search: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(JobApplication).filter(JobApplication.user_id == current_user.id)
    if status_filter:
        query = query.filter(JobApplication.status.ilike(status_filter))
    if search:
        query = query.filter((JobApplication.company.ilike(f"%{search}%")) | (JobApplication.role.ilike(f"%{search}%")))
    return query.order_by(JobApplication.id.desc()).all()

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(JobApplication).filter(JobApplication.id == application_id, JobApplication.user_id == current_user.id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, application_data: ApplicationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(JobApplication).filter(JobApplication.id == application_id, JobApplication.user_id == current_user.id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    for field, value in application_data.model_dump(exclude_unset=True).items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application

@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(JobApplication).filter(JobApplication.id == application_id, JobApplication.user_id == current_user.id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return {"message": "Application deleted successfully"}
