# Architecture

## Overview

Mini DBaaS is a Database as a Service prototype built with FastAPI and PostgreSQL. It provides a centralized API to manage database instances, users, authentication and database provisioning.

The platform separates metadata management from tenant database storage.

## Core components

- **Backend:** FastAPI application responsible for authentication, authorization, database management and provisioning.
- **Control Database:** PostgreSQL database storing platform metadata, users, roles, database registrations and ownership information.
- **Managed Database:** PostgreSQL instance hosting the databases provisioned through the platform.
- **Infrastructure:** Docker Compose for local development, Kubernetes manifests and Helm charts for container orchestration.

## Database architecture

The platform uses two PostgreSQL instances with different responsibilities:

- **Control DB:** stores users, permissions, ownership and registered databases.
- **Managed DB:** hosts the actual databases managed by the platform.

The backend connects to both instances and coordinates provisioning operations.

## Infrastructure evolution

The infrastructure was developed incrementally:

1. **Docker Compose:** initial local environment for developing and testing the application and PostgreSQL instances.
2. **Kubernetes:** container orchestration manifests were introduced to deploy the backend and PostgreSQL instances.
3. **Helm:** PostgreSQL Kubernetes resources were abstracted into reusable charts with separate configurations for the control and managed databases.
4. **Terraform:** planned future work to automate infrastructure provisioning.

The Terraform deployment still requires further validation, particularly PostgreSQL schema initialization and persistent storage integration.

## Future improvements

- Database sharing and Row-Level Security (RLS).
- MCP integration.
- Complete Kubernetes persistence and initialization workflow.
- Terraform infrastructure provisioning.
- Internal TLS communication.
- GitOps deployment with ArgoCD.