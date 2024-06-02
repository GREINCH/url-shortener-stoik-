"""
URLs Data Access

Interact with the database, including creating tables, managing database sessions, and performing CRUD operations
on the 'urls' table.
"""

from typing import Generator, Optional
import logging
import os
from datetime import datetime

from sqlalchemy import create_engine, Table, Column, String, MetaData, DateTime, Integer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/api_data.db")
metadata = MetaData()

urls = Table(
    "urls", metadata,
    Column("slug", String, primary_key=True),
    Column("long_url", String, nullable=False),
    Column("expires_at", DateTime, nullable=True),
    Column("click_count", Integer, default=0)
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """
    Generate a database session.

    Yields:
        Session: SQLAlchemy database session.

    Raises:
        SQLAlchemyError: If there is an error connecting to the database.
    """
    db: Optional[Session] = None
    try:
        db = SessionLocal()
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise
    finally:
        if db:
            db.close()


def insert_url(slug: str, long_url: str, db: Session, expires_at: Optional[datetime] = None) -> None:
    """
    Insert a new URL into the 'urls' table.

    Args:
        slug (str): The slug for the shortened URL.
        long_url (str): The original long URL.
        db (Session): SQLAlchemy database session.
        expires_at (Optional[datetime]): Expiration date for the URL, optional.
    """
    db.execute(urls.insert().values(slug=slug, long_url=long_url, expires_at=expires_at))
    db.commit()


def get_url(slug: str, db: Session) -> Optional[dict]:
    """
    Retrieve a URL from the 'urls' table by its slug.

    Args:
        slug (str): The slug of the shortened URL.
        db (Session): SQLAlchemy database session.

    Returns:
        Optional[dict]: The original long URL if found, otherwise None.
    """
    result = db.execute(urls.select().where(urls.c.slug == slug)).fetchone()
    if result:
        db.execute(urls.update().where(urls.c.slug == slug).values(click_count=urls.c.click_count + 1))
        db.commit()
    return result


def get_slug_by_url(long_url: str, db: Session) -> Optional[str]:
    """
    Retrieve the slug associated with a given long URL from the 'urls' table.

    Args:
        long_url (str): The original long URL.
        db (Session): SQLAlchemy database session.

    Returns:
        Optional[str]: The slug if found, otherwise None.
    """
    result = db.execute(urls.select().where(urls.c.long_url == long_url)).fetchone()
    return result
