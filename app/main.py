from email.mime import base
from fastapi import FastAPI

from app.core.database import engine, Base
from app.models import user , task

app = FastAPI(
    title="Todo List",
    version="1.0.0",
    description="FastAPI Todo List API",
)

Base.metadata.create_all(engine)