"""
URL Shortener API

FastAPI application and endpoints for shortening URLs and redirecting to the original long URLs based on slugs.

Endpoints:
- /shorten: Shorten a given URL.
- /{slug}: Redirect to the original long URL based on the slug.
"""

import logging
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, AnyHttpUrl
from sqlalchemy.orm import Session
from typing import Optional

from database.data_access import get_db
from services.url_service import shorten_url, fetch_long_url

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UrlRequest(BaseModel):
    url: AnyHttpUrl
    expires_in_days: Optional[int] = None  # Specify that expires_in_days can be None


class UrlResponse(BaseModel):
    short_url: str


@app.post("/shorten", response_model=UrlResponse)
def api_shorten_url(request: UrlRequest, db: Session = Depends(get_db)) -> UrlResponse:
    """
    API endpoint to shorten a given URL.

    Args:
        request (UrlRequest): Request body containing the long URL.
        db (Session): SQLAlchemy database session.

    Returns:
        UrlResponse: Response body containing the shortened URL.

    Raises:
        HTTPException: If there is an error shortening the URL.
    """
    try:
        expires_at: Optional[datetime] = None
        if request.expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)

        short_url = shorten_url(str(request.url), db, expires_at)
        logger.info(f"Shortened URL: {short_url}")
        return UrlResponse(short_url=short_url)

    except Exception as e:
        logger.error(f"Error shortening URL: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/{slug}", response_class=RedirectResponse)
def api_redirect_url(slug: str, db: Session = Depends(get_db)) -> RedirectResponse:
    """
    API endpoint to redirect to the original long URL based on the given slug.

    Args:
        slug (str): The slug of the shortened URL.
        db (Session): SQLAlchemy database session.

    Returns:
        RedirectResponse: Redirects to the original long URL.

    Raises:
        HTTPException: If the URL is not found or if there is an error.
    """
    long_url = fetch_long_url(slug, db)
    if long_url:
        logger.info(f"Redirecting to long URL: {long_url}")
        return RedirectResponse(url=long_url)
    else:
        logger.warning(f"Slug not found or expired: {slug}")
        raise HTTPException(status_code=404, detail="URL not found or expired")


if __name__ == '__main__':
    import uvicorn
    import sys

    if 'debug' in sys.argv:
        # Debug mode
        uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
    else:
        uvicorn.run(app, host='0.0.0.0', port=8000)
