from fastapi import FastAPI
from src.licht.lib.db import get_db, init_db, close_db
from contextlib import asynccontextmanager
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "System Running"}