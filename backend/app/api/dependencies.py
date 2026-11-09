
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.permissions import Permission, require_permission
from app.repositories import user_repository
from app.models.user import User


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id: UUID = decode_access_token(credentials.credentials)
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    user = user_repository.get_by_id(db, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user


def require_permission_dependency(permission: Permission):
    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        require_permission(
            current_user.role,
            permission,
        )
        return current_user

    return dependency


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    require_permission(
        current_user.role,
        Permission.USER_MANAGE,
    )
    return current_user
