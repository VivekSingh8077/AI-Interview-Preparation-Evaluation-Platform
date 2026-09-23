import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.core.config import get_settings
from app.database.base import Base
from app.database.session import engine
from app.api import auth
import app.models  # noqa: F401  (registers all ORM models on Base.metadata)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-interview-system")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev convenience: create tables if they don't exist yet.
    # In production, use Alembic migrations instead of relying on this.
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created.")
    except OperationalError as e:
        logger.error(
            "Could not connect to the database at startup. "
            "Is PostgreSQL running and DATABASE_URL correct? Error: %s", e
        )
    yield


app = FastAPI(
    title="AI Interview Evaluation & Feedback System",
    description="NLP/Transformer-based mock interview evaluation platform.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    # Never leak stack traces / internals to the client (§25).
    logger.exception("Unhandled exception on %s", request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
