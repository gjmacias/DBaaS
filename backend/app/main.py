from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health, auth, databases, users
from app.core.database import Base, engine
from app.models import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Mini DBaaS",
    description="Database as a Service platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(databases.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")