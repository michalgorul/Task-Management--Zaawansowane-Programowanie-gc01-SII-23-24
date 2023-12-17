from fastapi import FastAPI

from app.database.database import engine
from app.database.models import Base
from app.user.router import router as user_router
from app.task.router import router as task_router


app = FastAPI(
    title="Task Management API",
    description="REST API for managing tasks",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
)


app.include_router(user_router)
app.include_router(task_router)


Base.metadata.create_all(engine)
