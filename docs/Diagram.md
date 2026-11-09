# Architecture Diagram

## High-level architecture

```mermaid
flowchart TB
    Client[API Client / Swagger UI]

    subgraph Backend["FastAPI Backend"]
        API[REST API]
        Auth[Authentication & Authorization]
        Provisioning[Database Provisioning]
        API --> Auth
        API --> Provisioning
    end

    subgraph PostgreSQL["PostgreSQL Infrastructure"]
        Control[(Control DB<br/>Users, Roles, Metadata)]
        Managed[(Managed DB<br/>Tenant Databases)]
    end

    Client --> API
    Auth --> Control
    Provisioning --> Control
    Provisioning --> Managed
```

## Database provisioning flow

```mermaid
sequenceDiagram
    participant C as API Client
    participant B as FastAPI Backend
    participant A as Authorization
    participant DB as Control DB
    participant M as Managed DB

    C->>B: POST /api/v1/databases
    B->>A: Validate JWT and permissions
    A-->>B: Authorized
    B->>M: CREATE DATABASE
    M-->>B: Database created
    B->>DB: Register database and owner
    DB-->>B: Metadata saved
    B-->>C: Success response
```

## Infrastructure evolution

```mermaid
flowchart LR
    Local[Docker Compose<br/>Local development]
    K8s[Kubernetes<br/>Container orchestration]
    Helm[Helm<br/>Reusable PostgreSQL charts]
    Terraform[Terraform<br/>Future infrastructure provisioning]

    Local --> K8s
    K8s --> Helm
    Helm -.-> Terraform
```

## Notes

- Docker Compose is the initial and validated local deployment environment.
- Kubernetes manifests are available.
- Helm charts abstract PostgreSQL resources for the control and managed instances.
- Terraform is planned for future infrastructure provisioning.