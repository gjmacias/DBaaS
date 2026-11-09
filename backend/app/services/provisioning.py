
import logging

import psycopg
from psycopg import sql

from app.core.config import MANAGED_DB_CONFIG


logger = logging.getLogger(__name__)


def provision_database(database_name: str) -> None:
    logger.info("Starting database provisioning: %s", database_name)

    try:
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

        logger.info("Database provisioned successfully: %s", database_name)

    except Exception:
        logger.exception("Database provisioning failed: %s", database_name)
        raise


def deprovision_database(database_name: str) -> None:
    logger.info("Starting database deprovisioning: %s", database_name)

    try:
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

        logger.info("Database deprovisioned successfully: %s", database_name)

    except Exception:
        logger.exception("Database deprovisioning failed: %s", database_name)
        raise
