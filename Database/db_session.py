# Database/db_session.py
from __future__ import annotations
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from Database.Base import Base
from dotenv import load_dotenv
from os import getenv
from contextlib import contextmanager

# Load environment variables
load_dotenv()
USERNAME: str | None = getenv("DATABASE_USERNAME")
PASSWORD: str | None = getenv("DATABASE_PASSWORD")
HOST: str | None = getenv("DATABASE_HOST")
DATABASE: str | None = getenv("DATABASE_NAME")

# Construct the database URL
DATABASE_URL: str = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"

# Create SQLAlchemy engine
engine: Engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,   # Keeps connections alive
    pool_recycle=3600,    # Recycle every hour
)

# Create session factory
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for safe SQLAlchemy session handling.

    Yields:
        Session: an active SQLAlchemy session.

    Usage:
        with get_session() as session:
            player = session.query(Player).first()
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db() -> None:
    """
    Creates all database tables.
    Should be run once at app startup or setup.
    """
    from Database import (
        Player, Role, VipRole, VipAssignment, Activity,
        DiscordTicket, DiscordTicketLog
    )
    Base.metadata.create_all(bind=engine)