
import getpass
import sys

from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import User, Database


def get_validated_password() -> str | None:
    """Ask for a password and validate it. Returns None if empty."""

    password = getpass.getpass("Admin password: ")

    if not password:
        return None

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return None

    confirmation = getpass.getpass("Confirm password: ")

    if password != confirmation:
        print("Passwords do not match.")
        return None

    return password


def create_admin(db: Session) -> None:
    """Create the initial admin if no users exist."""

    existing_user = db.query(User).first()

    if existing_user is not None:
        print("Users already exist. Admin creation is disabled.")
        return

    username = input("Admin username: ").strip()

    if len(username) < 3 or len(username) > 50:
        print("Username must contain between 3 and 50 characters.")
        return

    password = get_validated_password()

    if password is None:
        print("Admin creation cancelled.")
        return

    admin = User(
        username=username,
        password_hash=get_password_hash(password),
        role="admin",
        is_active=True,
    )

    db.add(admin)
    db.commit()

    print(f"Admin '{username}' created successfully.")


def change_admin_password(db: Session) -> None:
    """Change the password of an existing admin."""

    admin = db.query(User).filter(User.role == "admin").first()

    if admin is None:
        print("No admin account found.")
        return

    print(f"Admin account found: '{admin.username}'")

    change = input("Do you want to change the password? [y/N]: ").strip().lower()

    if change not in ("y", "yes", "s", "si", "sí"):
        print("Password unchanged.")
        return

    password = get_validated_password()

    if password is None:
        print("Password unchanged.")
        return

    admin.password_hash = get_password_hash(password)
    db.commit()

    print(f"Password for admin '{admin.username}' changed successfully.")


def main() -> None:
    db = SessionLocal()

    try:
        Base.metadata.create_all(bind=engine)

        existing_admin = db.query(User).filter(User.role == "admin").first()

        if existing_admin is not None:
            change_admin_password(db)
        else:
            create_admin(db)

    except Exception as error:
        db.rollback()
        print(f"Admin operation failed: {error}", file=sys.stderr)
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
