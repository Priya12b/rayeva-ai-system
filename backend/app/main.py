from fastapi import FastAPI
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.models import product, proposal, ai_log
import app.routers.category as category
import app.routers.proposal as proposal_router
import logging
import os
from app.database import init_db
from seed_db import seed_database

init_db()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Rayeva AI System",
    description="AI-powered sustainable commerce platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow React frontend (localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(category.router, prefix="/ai", tags=["AI - Category Generator"])
app.include_router(proposal_router.router, prefix="/ai", tags=["AI - Proposal Generator"])

# Health check endpoint
@app.get("/", tags=["Health"])
def root():
    """Health check endpoint - system is running"""
    return {
        "message": "Rayeva AI System Running",
        "version": "1.0.0",
        "status": "healthy"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🌱 Rayeva AI System starting up...")
    logger.info("📚 API Documentation: http://localhost:8000/docs")

    auto_seed_enabled = os.getenv("AUTO_SEED_ON_STARTUP", "true").lower() == "true"
    if auto_seed_enabled:
        try:
            seed_database(reset=False)
            logger.info("✅ Auto-seed check completed")
        except Exception as e:
            logger.error(f"❌ Auto-seed failed: {e}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Rayeva AI System shutting down...")
