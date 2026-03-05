from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "not_started"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    job_site_id: int

    class Config:
        from_attributes = True

class JobSiteCreate(BaseModel):
    name: str
    location: str
    status: str = "active"

class JobSiteResponse(BaseModel):
    id: int
    name: str
    location: str
    status: str
    owner_id: int
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True