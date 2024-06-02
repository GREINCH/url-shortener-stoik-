# URL Shortener API

## Introduction
The URL Shortener API is a FastAPI application designed to shorten URLs and provide redirection to the original URLs based on unique slugs. This API is ideal for applications that need to condense long URLs into manageable, short links that are easier to share and handle.

## Features
- **Shorten URL**: Converts a long URL into a short URL with an expiration option.
- **Redirect URL**: Redirects to the original long URL based on a unique slug.

## Requirements
- Python 3.10 or higher
- FastAPI
- Uvicorn
- SQLAlchemy

## Local Setup
Follow these steps to set up the project locally:

### 1. Clone the repository:
   ```
   git clone https://github.com/GREINCH/url-shortener-stoik-
   cd url-shortener-stoik-/
   ```


### 2. Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies:

```
pip install -r requirements.txt
```

### 4. Run the application:

##### Locally
```
uvicorn api:app --reload  # The `--reload` flag enables hot reloading during development.
The API will be available at http://127.0.0.1:8000.
```

##### Using Docker

To containerize and run the API using Docker, follow these instructions:

Build the Docker image:

```
docker build -t url-shortener .
```

Run the container:

```
docker run -p 80:80 --name url-shortener-instance url-shortener
The API will be accessible at http://127.0.0.1:80.
```
- The API documentation is here:
```
The API will be accessible at http://127.0.0.1:80/docs.
The API will be accessible at http://127.0.0.1:80/redoc.
```

### 5. API Endpoints

##### Shorten URL

- Endpoint: POST /shorten
- Body:
```
{
  "url": "https://youtube.fr",
  "expires_in_days": 10
}
```
- Description: Shortens the provided URL and optionally sets an expiration date.

##### Redirect URL
- Endpoint: GET /{slug}
- Description: Redirects to the original URL associated with the provided slug. For example:
```
  http://127.0.0.1:80/A6H432
  ```