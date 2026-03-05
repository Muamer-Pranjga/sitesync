from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="worker")

    job_sites = relationship("JobSite", back_populates="owner")

class JobSite(Base):
    __tablename__ = "job_sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default="active")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="job_sites")
    tasks = relationship("Task", back_populates="job_site")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="not_started")
    job_site_id = Column(Integer, ForeignKey("job_sites.id"))

    job_site = relationship("JobSite", back_populates="tasks")