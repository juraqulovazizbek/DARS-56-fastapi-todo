from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import router

app = FastAPI(title="Todo List", version="1.0.0", description="FastAPI Todo List API")
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(router, prefix="/api")
