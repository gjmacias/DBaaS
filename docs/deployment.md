# Deployment and CI/CD

## Overview

The project uses Docker for containerization and GitHub Actions for Continuous Integration and Continuous Deployment (CI/CD).

The infrastructure evolved from a local Docker Compose environment to Kubernetes manifests and Helm charts.

## Docker Compose

Docker Compose was the initial deployment environment, used for local development and integration testing.

The environment includes:

- **Backend:** FastAPI application.
- **Control DB:** PostgreSQL instance for platform metadata.
- **Managed DB:** PostgreSQL instance hosting tenant databases.

Persistent Docker volumes are used to retain PostgreSQL data.

Configuration and credentials are loaded from an external `.env` file, which is excluded from version control.

Start the environment from the project root:

```bash
docker-compose -f infrastructure/docker/docker-compose.yml up -d
```

## Kubernetes

Kubernetes manifests are available under `infrastructure/kubernetes/manifests/`.

They define deployments, services, configuration and persistent storage for the backend and PostgreSQL instances.

The PostgreSQL workloads use StatefulSets and PersistentVolumeClaims.

## Helm

Helm charts were introduced to abstract PostgreSQL Kubernetes resources and avoid duplicating configuration.

The PostgreSQL chart supports separate configurations for:

- Control Database.
- Managed Database.

Chart files are located under `infrastructure/helm/postgres/`.

## CI/CD pipeline

GitHub Actions automates testing and image publication.

The current workflow:

1. Runs on pushes and pull requests.
2. Sets up Python 3.12.
3. Installs backend dependencies.
4. Runs compilation checks.
5. Executes the automated test suite.
6. Publishes a Docker image to GitHub Container Registry (GHCR) when changes are pushed to `main`, provided the tests pass.

Images are published with:

- The commit SHA.
- The `latest` tag.

The published image can then be used by Docker Compose and Kubernetes deployments.

## Future improvements

- **ArgoCD:** introduce GitOps-based deployment and automatic synchronization with the repository.
- **Terraform:** automate infrastructure provisioning.
- **TLS:** enable encrypted internal communication between services.
- **CD improvements:** automate deployment updates after successful image publication and improve rollback capabilities.