
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.schemas.user import UserLogin, TokenResponse


class InvalidCredentials(Exception):
    pass


def authenticate_user(
    db: Session,
    credentials: UserLogin,
):
    user = user_repository.get_by_username(
        db,
        credentials.username,
    )

    if user is None:
        raise InvalidCredentials("Invalid username or password")

    if not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise InvalidCredentials("Invalid username or password")

    if not user.is_active:
        raise InvalidCredentials("User account is disabled")

    return user


def login(
    db: Session,
    credentials: UserLogin,
) -> TokenResponse:
    user = authenticate_user(db, credentials)

    token = create_access_token(user.id)

    return TokenResponse(
        access_token=token,
    )
