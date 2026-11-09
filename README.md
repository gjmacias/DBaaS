# Mini DBaaS

A lightweight Database as a Service prototype built with **FastAPI**, **PostgreSQL** and **Docker**.

The platform provides an API to manage databases, users, authentication and database provisioning, separating platform metadata from tenant database storage.

## Architecture

The platform uses two PostgreSQL instances:

- **Control DB:** stores users, roles, permissions and database metadata.
- **Managed DB:** hosts provisioned tenant databases.

The backend coordinates both instances through a REST API.

## Main features

- JWT authentication and role-based access control (`admin`, `user`, `viewer`).
- Database CRUD operations and provisioning.
- User creation and listing for administrators.
- Docker Compose local environment.
- Kubernetes manifests and Helm charts.
- Automated tests and CI/CD with GitHub Actions.
- Docker image publication to GitHub Container Registry.
- PostgreSQL backups and restore testing.
- Health checks, structured application logs and Prometheus metrics.

## Technology stack

| Area | Technology |
|---|---|
| Backend | Python 3.12, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT, Argon2 |
| Containers | Docker, Docker Compose |
| Orchestration | Kubernetes, Helm |
| CI/CD | GitHub Actions, GHCR |
| Backups | pg_dump, pg_restore |
| Observability | Python logging, Prometheus instrumentation |
| Testing | pytest |

## Getting started

The initial development environment uses Docker Compose.

Create the local environment configuration at:

`infrastructure/docker/.env`

Start the services:

```bash
docker-compose -f infrastructure/docker/docker-compose.yml up -d
```

The API is available at:

`http://localhost:8000`

Interactive API documentation:

`http://localhost:8000/docs`

## Documentation

- [Architecture](docs/architecture.md)
- [Architecture diagrams](docs/Diagram.md)
- [API documentation](docs/api.md)
- [Security](docs/security.md)
- [Deployment and CI/CD](docs/deployment.md)
- [Operations and observability](docs/operations.md)
- [Architecture decisions](docs/decisions/ADR-001-infrastructure-evolution.md)

## Roadmap

- Database sharing and PostgreSQL Row-Level Security (RLS).
- MCP integration.
- GitOps deployments with ArgoCD.
- Infrastructure provisioning with Terraform.
- Internal TLS communication.
- Centralized metrics collection and dashboards.

## Project status

This repository contains an interview-oriented DBaaS prototype. Docker Compose is the validated local environment. Kubernetes and Helm resources are available but still require further integration and persistence validation.

It is not intended to be considered production-ready.