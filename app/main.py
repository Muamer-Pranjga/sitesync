from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SiteSync", description="Job Site Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed = auth.hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/job-sites", response_model=list[schemas.JobSiteResponse])
def get_job_sites(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    return db.query(models.JobSite).all()

@app.post("/job-sites", response_model=schemas.JobSiteResponse)
def create_job_site(job_site: schemas.JobSiteCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.username == current_user["sub"]).first()
    new_site = models.JobSite(name=job_site.name, location=job_site.location, status=job_site.status, owner_id=user.id)
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site

@app.post("/job-sites/{site_id}/tasks", response_model=schemas.TaskResponse)
def create_task(site_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    job_site = db.query(models.JobSite).filter(models.JobSite.id == site_id).first()
    if not job_site:
        raise HTTPException(status_code=404, detail="Job site not found")
    new_task = models.Task(title=task.title, description=task.description, status=task.status, job_site_id=site_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/job-sites/{site_id}/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(site_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    return db.query(models.Task).filter(models.Task.job_site_id == site_id).all()

@app.put("/job-sites/{site_id}", response_model=schemas.JobSiteResponse)
def update_job_site(site_id: int, job_site: schemas.JobSiteCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    site = db.query(models.JobSite).filter(models.JobSite.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Job site not found")
    site.name = job_site.name
    site.location = job_site.location
    site.status = job_site.status
    db.commit()
    db.refresh(site)
    return site

@app.delete("/job-sites/{site_id}")
def delete_job_site(site_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    site = db.query(models.JobSite).filter(models.JobSite.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Job site not found")
    db.delete(site)
    db.commit()
    return {"message": "Job site deleted"}

@app.put("/job-sites/{site_id}/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(site_id: int, task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    existing_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.job_site_id == site_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status
    db.commit()
    db.refresh(existing_task)
    return existing_task

@app.delete("/job-sites/{site_id}/tasks/{task_id}")
def delete_task(site_id: int, task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.job_site_id == site_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}