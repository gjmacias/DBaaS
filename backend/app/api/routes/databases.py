from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.database import DatabaseCreate, DatabaseResponse
from app.services import database_manager

router = APIRouter(
    prefix="/databases",
    tags=["Databases"],
)


@router.post(
    "",
    response_model=DatabaseResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_database(
    request: DatabaseCreate,
    db: Session = Depends(get_db)
):
    try:
        return database_manager.request_database(db, request)
    except database_manager.DatabaseAlreadyExists as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    except database_manager.ProvisioningError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error)
        )


@router.get(
    "",
    response_model=list[DatabaseResponse],
)
def list_databases(
    db: Session = Depends(get_db),
):
    return database_manager.list_databases(db)


@router.get(
    "/{database_id}",
    response_model=DatabaseResponse,
)
def get_database(
    database_id: UUID,
    db: Session = Depends(get_db),
):
    database = database_manager.get_database(db, database_id)

    if database is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database not found",
        )

    return database


@router.delete(
    "/{database_id}",
    response_model=DatabaseResponse
)
def delete_database(
    database_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        database = database_manager.delete_database(db, database_id)

        if database is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database not found"
            )

        return database

    except database_manager.DeprovisioningError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error)
        )