import psycopg
from psycopg import sql

from app.core.config import MANAGED_DB_CONFIG


def provision_database(database_name: str) -> None:
    with psycopg.connect(
        host=MANAGED_DB_CONFIG["host"],
        port=MANAGED_DB_CONFIG["port"],
        dbname=MANAGED_DB_CONFIG["database"],
        user=MANAGED_DB_CONFIG["user"],
        password=MANAGED_DB_CONFIG["password"],
        autocommit=True,
    ) as connection:
        query = sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(database_name)
        )
        connection.execute(query)



def deprovision_database(database_name: str) -> None:
    with psycopg.connect(
        host=MANAGED_DB_CONFIG["host"],
        port=MANAGED_DB_CONFIG["port"],
        dbname=MANAGED_DB_CONFIG["database"],
        user=MANAGED_DB_CONFIG["user"],
        password=MANAGED_DB_CONFIG["password"],
        autocommit=True,
    ) as connection:
        query = sql.SQL(
            "DROP DATABASE IF EXISTS {} WITH (FORCE)"
        ).format(
            sql.Identifier(database_name)
        )

        connection.execute(query)