# Operations and Observability

## Backups

The project includes an automated PostgreSQL backup script located at:

`scripts/backup.sh`

The script:

- Uses `pg_dump` to generate PostgreSQL backups.
- Uses PostgreSQL custom format (`-Fc`).
- Stores backup files under `backups/`.
- Adds timestamps to backup filenames.
- Removes backups older than seven days.

Backups are excluded from Git through `.gitignore`.

## Scheduling

Backups are scheduled using cron on the host machine.

The current configuration runs a daily backup at 02:00.

The host must be running and Docker Compose must be available when the scheduled task executes.

## Restore procedure

Backups can be restored using `pg_restore`.

Example:

```bash
docker-compose -f infrastructure/docker/docker-compose.yml exec -T managed-db sh -c \
'pg_restore -U "$POSTGRES_USER" -d restore_database' \
< backups/backup_file.dump
```

Restoration has been tested against a separate database to verify that backup contents can be recovered without modifying existing tenant databases.

Periodic restore testing is recommended. A backup is only useful if it can be restored successfully.

## Health checks

The backend exposes two health endpoints:

- `/health`: checks whether the API process is responding.
- `/ready`: checks whether the Control Database is reachable.

The readiness endpoint returns HTTP 503 when the Control Database cannot be reached.

## Logging

The application uses Python's standard logging module.

Logs include:

- Application startup and shutdown.
- Database provisioning operations.
- Database deprovisioning operations.
- Provisioning errors and their stack traces.

Logs are written to standard output, allowing Docker to collect them.

Sensitive information such as passwords and JWT tokens must not be logged.

## Metrics

The backend uses `prometheus-fastapi-instrumentator` to expose Prometheus metrics through:

`/metrics`

Available metrics include:

- HTTP request counters.
- HTTP request duration.
- Request and response sizes.
- Python garbage collection statistics.
- Process CPU and memory usage.

The endpoint exposes metrics in Prometheus format.

A Prometheus server and Grafana dashboard are not currently part of the deployed monitoring stack.

## Operational limitations

- Backups currently depend on the host machine and Docker Compose.
- Backup files are stored locally and do not yet have off-site replication.
- Backup encryption and automated restore validation are future improvements.
- Prometheus metrics are exposed but not yet collected by a monitoring server.
- Kubernetes backup and recovery procedures still require implementation and validation.