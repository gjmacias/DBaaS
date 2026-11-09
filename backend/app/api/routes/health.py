from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import engine

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """Liveness: the API process is responding."""
    return {
        "status": "healthy",
        "service": "mini-dbaas-api"
    }


@router.get("/ready")
def readiness_check():
    """Readiness: the control database is reachable."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "checks": {
                "control_db": "ok"
            }
        }

    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {
                    "control_db": "error"
                }
            }
        )