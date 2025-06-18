from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Dog
from app.config import settings

client: AsyncIOMotorClient | None = None

async def init_db():
    global client
    client = AsyncIOMotorClient(settings.mongodb_uri)
    await init_beanie(database=client[settings.mongodb_db], document_models=[Dog])

async def close_db():
    global client
    if client:
        client.close()
