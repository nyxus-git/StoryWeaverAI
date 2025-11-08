from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import create_tables

from routers import story as story_router
from routers import job as job_router

from models import story as story_model
from models import job as job_model

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
def on_startup():
    create_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story_router.router, prefix=settings.API_PREFIX)
app.include_router(job_router.router, prefix=settings.API_PREFIX)