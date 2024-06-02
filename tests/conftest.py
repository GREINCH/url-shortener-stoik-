import os

import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

# Setting the environment variable for the database URL
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from database.data_access import metadata, engine, get_db  # Imported after setting environment variable
from api import app


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Set up the test database before any tests run and ensure it is deleted after all tests are done.
    """
    # Ensure the test database exists and create all tables
    metadata.create_all(engine)

    # Yield to run the tests
    yield

    # Clean up: Drop all tables
    metadata.drop_all(engine)

    # Remove the test database file
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture(scope="function")
def db_session():
    """
    Generate a database session for tests.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))

    yield session

    session.remove()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def override_get_db(db_session):
    """
    Override the get_db dependency to use the test database session.
    """

    def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.remove()

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
