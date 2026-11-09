
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

def create(
    db: Session,
    data: UserCreate,
    password_hash: str,
    role: str = "user",
) -> User:
    user = User(
        username=data.username,
        password_hash=password_hash,
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_by_id(db: Session, user_id) -> User | None:
    statement = select(User).where(
        User.id == user_id
    )

    return db.scalar(statement)


def get_by_username(db: Session, username: str) -> User | None:
    statement = select(User).where(
        User.username == username
    )

    return db.scalar(statement)


def get_all(db: Session) -> list[User]:
    statement = select(User).order_by(User.created_at.desc())

    return list(db.scalars(statement).all())
