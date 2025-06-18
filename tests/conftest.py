import os
from dotenv import load_dotenv

# Load test environment variables BEFORE importing app code
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.test'), override=True)

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app

@pytest_asyncio.fixture
async def async_client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
