from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import database_repository
from app.schemas.database import DatabaseCreate
from app.services.provisioning import (
    provision_database,
    deprovision_database,
)


class ProvisioningError(Exception):
    pass

class DatabaseAlreadyExists(Exception):
    pass

class DeprovisioningError(Exception):
    pass

def request_database(db: Session, request: DatabaseCreate, owner_id):
    database = None

    try:
        database = database_repository.create(db, request, owner_id)

    except IntegrityError as error:
        db.rollback()
        raise DatabaseAlreadyExists(
            f"Database '{request.name}' already exists"
        ) from error

    
    try:
        database.status = "PROVISIONING"
        db.commit()

        provision_database(database.name)

        database.status = "READY"
        db.commit()

        db.refresh(database)
        return database

    except Exception as error:
        db.rollback()

        database = database_repository.get_by_id(db, database.id)

        if database is not None:
            database.status = "FAILED"
            db.commit()

        raise ProvisioningError(
            f"Could not provision database: {request.name}"
        ) from error


def get_database(db: Session, database_id):
    return database_repository.get_by_id(db, database_id)


def list_databases(db: Session):
    return database_repository.get_all(db)

def delete_database(db: Session, database_id):
    database = database_repository.get_by_id(db, database_id)

    if database is None:
        return None

    if database.status == "DELETED":
        return database

    try:
        database.status = "DELETING"
        db.commit()

        deprovision_database(database.name)

        database.status = "DELETED"
        db.commit()

        db.refresh(database)
        return database

    except Exception as error:
        db.rollback()

        database = database_repository.get_by_id(db, database_id)

        if database is not None:
            database.status = "FAILED"
            db.commit()

        raise DeprovisioningError(
            f"Could not delete database: {database_id}"
        ) from error