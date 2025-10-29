# models/job.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from db.database import Base


class StoryJob(Base):
    __tablename__ = "story_jobs"

    id = Column(Integer, index=True)  
    job_id = Column(String, primary_key=True, index=True)  
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String, default="pending")  
    story_id = Column(Integer, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)