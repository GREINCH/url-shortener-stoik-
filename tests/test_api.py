"""
Integration tests for the URL shortening service API.

Tests cover:
- Shortening a URL: Ensures that providing a long URL to the `/shorten` endpoint correctly returns a shortened URL.
- Redirecting from a shortened URL: Checks that accessing a shortened URL correctly redirects to the original long URL.
"""

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_shorten_url():
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert "short_url" in response.json()
    assert response.json()["short_url"].startswith("https://tiny.io/")


def test_redirect_url(override_get_db):
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    short_url = response.json()["short_url"]
    slug = short_url.split("/")[-1]

    # Attempt to fetch the redirect URL
    response = client.get(f"/{slug}", allow_redirects=False)  # Do not follow redirects
    assert response.status_code == 307  # Temporary redirect status
    assert response.headers['location'] == "https://example.com/"  # Check redirect target
