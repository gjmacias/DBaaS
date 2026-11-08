from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import CONTROL_DB_CONFIG


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=CONTROL_DB_CONFIG["user"],
    password=CONTROL_DB_CONFIG["password"],
    host=CONTROL_DB_CONFIG["host"],
    port=CONTROL_DB_CONFIG["port"],
    database=CONTROL_DB_CONFIG["database"],
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()