import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    """
    Test client for FastAPI application.
    """
    with TestClient(app) as c:
        yield c
