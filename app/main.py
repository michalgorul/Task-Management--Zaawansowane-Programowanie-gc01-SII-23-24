from fastapi import FastAPI

from app.api.task.router import router as task_router
from app.api.user.router import router as user_router
from app.database.database import Base
from app.database.database import engine

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
