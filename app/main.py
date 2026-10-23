from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes import auth, applications, interviews

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application & Interview Management API",
    version="1.0.0",
    description="Backend API for managing job applications and interviews."
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(interviews.router)

@app.get("/")
def home():
    return {"message": "Job Application API is running"}
