from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "Applied"

class ApplicationUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    status: str | None = None

class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company: str
    role: str
    status: str
    user_id: int

class InterviewCreate(BaseModel):
    application_id: int
    interview_date: datetime
    interview_type: str
    notes: str | None = None

class InterviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    application_id: int
    interview_date: datetime
    interview_type: str
    notes: str | None
