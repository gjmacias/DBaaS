from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database import Database
from app.schemas.database import DatabaseCreate


def create(db: Session, data: DatabaseCreate) -> Database:
    database = Database(**data.model_dump())

    db.add(database)
    db.commit()
    db.refresh(database)

    return database


def get_by_id(db: Session, database_id) -> Database | None:
    statement = select(Database).where(
        Database.id == database_id
    )

    return db.scalar(statement)


def get_all(db: Session) -> list[Database]:
    statement = select(Database).order_by(Database.created_at.desc())

    return list(db.scalars(statement).all())