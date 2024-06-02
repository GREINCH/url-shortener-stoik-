"""
URL Shortening Service

Provides functions to shorten URLs and retrieve the original long URLs
based on generated slugs.

"""

from typing import Optional
import logging
import random
import string
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database.data_access import insert_url, get_url, get_slug_by_url

logger = logging.getLogger(__name__)


def generate_slug(length: int = 6) -> str:
    """
    Generate a random slug of given length.

    Args:
        length (int): Length of the generated slug (Default is 6).

    Returns:
        str: Generated slug.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def shorten_url(long_url: str, db: Session, expires_at: Optional[datetime] = None) -> str:
    """
    Shorten a long URL by generating a slug and storing it in the database.

    Args:
        long_url (str): The original long URL to shorten.
        db (Session): SQLAlchemy database session.
        expires_at (Optional[datetime]): Expiration date for the URL, optional.

    Returns:
        str: The shortened URL.

    Raises:
        SQLAlchemyError: If there is an error inserting the URL into the database.
    """
    existing_slug = get_slug_by_url(long_url, db)
    if existing_slug:
        return f"https://tiny.io/{existing_slug.slug}"
    slug = generate_slug()

    try:
        insert_url(slug, long_url, db, expires_at)
        short_url = f"https://tiny.io/{slug}"
        return short_url
    except SQLAlchemyError as e:
        logger.error(f"Error inserting URL into database: {e}")
        raise


def fetch_long_url(slug: str, db: Session) -> Optional[str]:
    """
    Retrieve the original long URL associated with a given slug from the database.

    Args:
        slug (str): The slug of the shortened URL.
        db (Session): SQLAlchemy database session.

    Returns:
        Optional[str]: The original long URL, or None if not found.

    Raises:
        SQLAlchemyError: If there is an error fetching the URL from the database.
    """
    try:
        result = get_url(slug, db)
        if result:
            if result.expires_at and result.expires_at < datetime.utcnow():
                logger.warning(f"URL expired: {slug}")
                return None
            return result.long_url
        return None
    except SQLAlchemyError as e:
        logger.error(f"Error fetching URL from database: {e}")
        raise
