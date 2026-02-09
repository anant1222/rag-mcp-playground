"""Main application entry point"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from app.routers.index import register_routers
from app.middleware.error_handler import setup_error_handlers
from app.utils.logger import setup_logger
from app.config import settings

# Setup logger
logger = setup_logger("app", level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler"""
    # Startup
    logger.info("Starting AI LLM API...")
    logger.info(f"OpenAI Model: {settings.OPENAI_MODEL}")
    logger.info("Application started successfully")

    yield

    # Shutdown
    logger.info("Shutting down AI LLM API...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="AI LLM API",
    description="Production-ready API endpoints for LLM interactions: /ask, /chat, and /stream",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Register routers
register_routers(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
