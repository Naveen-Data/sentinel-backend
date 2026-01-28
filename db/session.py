"""
Sentinel Database Session Management

This module handles PostgreSQL connection pooling and session management.

Design principles:
- Async-first (using asyncpg)
- Single source of truth
- Request-scoped sessions
- Connection pooling
- Explicit lifecycle management
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------
# SQLAlchemy Base
# ---------------------------------------------------------------------

Base = declarative_base()

# ---------------------------------------------------------------------
# Database Engine
# ---------------------------------------------------------------------

settings = get_settings()

# Convert postgresql:// to postgresql+asyncpg:// to do async connections
database_url = settings.database_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# echo=settings.debug,  # Log SQL queries in debug mode
engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,
    max_overflow=10,
)

# ---------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# ---------------------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for the request lifecycle.
    
    Usage in FastAPI:
        @app.get("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    
    This ensures:
    - Session is created per request
    - Session is automatically closed
    - Exceptions trigger rollback
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

# ---------------------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------------------

async def init_db() -> None:
    """
    Initialize database (create tables if they don't exist).
    
    NOTE:
    - This is for development only
    - Production uses Alembic migrations
    - Called on application startup
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialization complete")
