"""
SQLAlchemy engine + session factory.

get_db() is used as a FastAPI dependency in route handlers so each
request gets its own session that is always closed afterwards, even
if an exception is raised mid-request.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # avoids stale-connection errors after DB idles
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
