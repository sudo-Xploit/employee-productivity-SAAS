from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import asynccontextmanager
from typing import Generator, AsyncGenerator

from app.core.config import settings

# Configure connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Check connection validity before using it
    pool_size=settings.DB_POOL_SIZE,  # Maximum number of connections
    max_overflow=settings.DB_MAX_OVERFLOW,  # Maximum number of connections that can be created beyond pool_size
    pool_timeout=settings.DB_POOL_TIMEOUT,  # Seconds to wait before timing out on getting a connection
    pool_recycle=settings.DB_POOL_RECYCLE,  # Seconds after which a connection is recycled
    echo=settings.DB_ECHO,  # Log SQL queries (set to False in production)
    poolclass=QueuePool  # Use QueuePool for connection pooling
)

# Add event listeners for connection pool monitoring
@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    print("Connection created")

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    print("Connection checked out")

@event.listens_for(engine, "checkin")
def checkin(dbapi_connection, connection_record):
    print("Connection checked in")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Synchronous database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For async endpoints
async def get_async_db() -> AsyncGenerator:
    """Asynchronous database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()