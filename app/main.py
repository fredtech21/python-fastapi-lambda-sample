from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db, close_db
from app.routes.dogs import router as dog_router
from mangum import Mangum

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(dog_router)

handler = Mangum(app)