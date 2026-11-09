#!/bin/bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <database_name>"
    exit 1
fi

DATABASE_NAME="$1"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups"
BACKUP_FILE="${BACKUP_DIR}/${DATABASE_NAME}_${TIMESTAMP}.dump"

mkdir -p "$BACKUP_DIR"

echo "Starting backup of ${DATABASE_NAME}..."

docker-compose -f infrastructure/docker/docker-compose.yml \
    exec -T managed-db sh -c \
    "pg_dump -U \"\$POSTGRES_USER\" -d \"$DATABASE_NAME\" -Fc" \
    > "$BACKUP_FILE"

if [ ! -s "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file is empty."
    rm -f "$BACKUP_FILE"
    exit 1
fi

echo "Backup completed successfully:"
echo "$BACKUP_FILE"
ls -lh "$BACKUP_FILE"

# Remove backups older than 7 days for this database
find "$BACKUP_DIR" \
    -type f \
    -name "${DATABASE_NAME}_*.dump" \
    -mmin +10080 \
    -delete

echo "Backup retention policy applied (7 days)."