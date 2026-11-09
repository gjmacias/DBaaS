
from enum import Enum

from fastapi import HTTPException, status


class Role(str, Enum):
    VIEWER = "viewer"
    USER = "user"
    ADMIN = "admin"


class Permission(str, Enum):
    DATABASE_READ = "database:read"
    DATABASE_CREATE = "database:create"
    DATABASE_DELETE = "database:delete"
    USER_MANAGE = "user:manage"


# Centralized role-permission mapping.
ROLE_PERMISSIONS = {
    Role.VIEWER: {
        Permission.DATABASE_READ,
    },
    Role.USER: {
        Permission.DATABASE_READ,
        Permission.DATABASE_CREATE,
        Permission.DATABASE_DELETE,
    },
    Role.ADMIN: {
        Permission.DATABASE_READ,
        Permission.DATABASE_CREATE,
        Permission.DATABASE_DELETE,
        Permission.USER_MANAGE,
    },
}


def has_permission(role: str, permission: Permission) -> bool:
    try:
        user_role = Role(role)
    except ValueError:
        return False

    return permission in ROLE_PERMISSIONS[user_role]


def require_permission(role: str, permission: Permission) -> None:
    if not has_permission(role, permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


def require_admin(role: str) -> None:
    require_permission(role, Permission.USER_MANAGE)
