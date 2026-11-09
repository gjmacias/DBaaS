import logging

from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI

from app.api.routes import health, auth, databases, users
from app.core.database import Base, engine
from app.core.logging_config import configure_logging
from app.models import Database


logger = logging.getLogger(__name__)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting Mini DBaaS API")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Stopping Mini DBaaS API")

app = FastAPI(
    title="Mini DBaaS",
    description="Database as a Service platform",
    version="0.1.0",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)

app.include_router(health.router)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(databases.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")