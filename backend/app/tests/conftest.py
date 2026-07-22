"""
conftest.py — Test configuration and fixtures.

Overrides the database dependency to use an isolated SQLite database
for tests, so tests never touch the real PostgreSQL database and can run
independently of each other.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database.dependencies import get_db
from app.main import app

# ── SQLite test engine ────────────────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def setup_test_db():
    """
    Create all tables before each test, drop them after.
    autouse=True means this runs automatically for every test function.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def override_get_db(setup_test_db):
    """Override the FastAPI get_db dependency to use the test database."""
    def _get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def db_session(setup_test_db):
    """Yield a raw SQLAlchemy session for direct DB manipulation in tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

