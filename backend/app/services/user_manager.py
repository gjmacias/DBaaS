
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserAlreadyExists(Exception):
    pass


def create_user(
    db: Session,
    request: UserCreate,
    role: str = "user",
):
    existing_user = user_repository.get_by_username(
        db,
        request.username,
    )

    if existing_user is not None:
        raise UserAlreadyExists(
            f"Username '{request.username}' already exists"
        )

    hashed_password = get_password_hash(request.password)

    try:
        return user_repository.create(
            db=db,
            data=request,
            password_hash=hashed_password,
            role=role,
        )

    except IntegrityError as error:
        db.rollback()
        raise UserAlreadyExists(
            f"Username '{request.username}' already exists"
        ) from error


def get_user_by_username(db: Session, username: str):
    return user_repository.get_by_username(db, username)


def get_user_by_id(db: Session, user_id):
    return user_repository.get_by_id(db, user_id)


def list_users(db: Session):
    return user_repository.get_all(db)
 