import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryResponse,
    CompleteStoryNodeResponse,
    CreateStoryRequest
)
from schemas.job import StoryJobsResponse
from core.story_generator import StoryGenerator

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@router.post("/create", response_model=StoryJobsResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    # --- PRINT 1 ---
    print(f"\n[DEBUG] 1. create_story endpoint HIT for theme: {request.theme}")

    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )

    db.add(job)
    db.commit()

    # --- PRINT 2 ---
    print(f"[DEBUG] 2. Job created with ID: {job_id}. Adding background task.")

    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    # --- PRINT 3 ---
    print(f"[DEBUG] 3. Returning job ID to frontend.\n")

    return job


def generate_story_task(job_id: str, theme: str, session_id: str):
    # --- PRINT 4 ---
    print(f"\n[DEBUG] 4. Background task STARTED for Job ID: {job_id}")

    db = SessionLocal()
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            # --- PRINT 5 ---
            print(f"[DEBUG] 5. ERROR: Job {job_id} not found in database.")
            return
        try:
            job.status = "in_progress"
            db.commit()
            
            # --- PRINT 6 ---
            print(f"[DEBUG] 6. Job {job_id} status set to 'in_progress'.")
            
            # --- PRINT 7 ---
            print(f"[DEBUG] 7. Calling StoryGenerator... (This is the long step)")
            
            story = StoryGenerator.generate_story(db, session_id, theme)

            # --- PRINT 8 ---
            print(f"[DEBUG] 8. StoryGenerator FINISHED. Story ID: {story.id}")

            job.story_id = story.id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
            
            # --- PRINT 9 ---
            print(f"[DEBUG] 9. Job {job_id} status set to 'completed'.\n")

        except Exception as e:
            # --- PRINT 10 (CRITICAL) ---
            print(f"\n[DEBUG] 10. !!!---CRITICAL ERROR---!!!")
            print(f"[DEBUG] Job {job_id} FAILED. Error: {str(e)}\n")
            
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()

# ... (rest of your file is unchanged) ...
@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=404, detail="Story Root Node not found")
    
    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        Session_id = story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )