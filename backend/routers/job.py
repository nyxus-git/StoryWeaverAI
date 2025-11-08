import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException , Cookie
from sqlalchemy.orm import Session
from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobsResponse

router = APIRouter(
    prefix = "/jobs",
    tags = ["jobs"]
)

@router.get("/{job_id}", response_model = StoryJobsResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    # --- PRINT 1: Show the poll request ---
    print(f"\n[POLL] Frontend is asking for Job ID: {job_id}")

    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    
    if not job:
        raise HTTPException(status = 404, detail = "job not found")
    
    # Force SQLAlchemy to get the latest data
    db.refresh(job)
    
    # --- PRINT 2: Show exactly what status is being sent ---
    print(f"[POLL] Refreshed data. Sending status: {job.status}")
    
    return job