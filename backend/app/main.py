import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.init_db import init_database
from app.api.auth import router as auth_router
from app.api.investigations import router as investigations_router
from app.api.events import router as events_router
from app.api.sessions import router as sessions_router
from app.api.ml import router as ml_router
from app.api.collector import router as collector_router
from app.api.admin import router as admin_router
from app.api.reports import router as reports_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("digital_fossil")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Digital Fossil Engine...")
    init_database()
    logger.info("Digital Fossil Engine initialized successfully.")
    yield
    logger.info("Shutting down Digital Fossil Engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Explainable Digital Activity Reconstruction Engine",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local Vite development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api/v1
api_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_prefix)
app.include_router(investigations_router, prefix=api_prefix)
app.include_router(events_router, prefix=api_prefix)
app.include_router(sessions_router, prefix=api_prefix)
app.include_router(ml_router, prefix=api_prefix)
app.include_router(collector_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)
app.include_router(reports_router, prefix=api_prefix)

@app.get("/")
def root():
    return {
        "project": "DIGITAL FOSSIL",
        "tagline": "Don't just show what happened. Reconstruct what likely happened — and prove why.",
        "status": "ONLINE",
        "docs_url": "/docs",
        "api_v1": api_prefix
    }
