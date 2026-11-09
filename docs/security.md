# Security

## Authentication

The backend uses JWT (JSON Web Tokens) for API authentication.

- Users authenticate through the login endpoint.
- Successful authentication returns an access token.
- Protected API endpoints require a valid Bearer token.
- JWT tokens are signed using the HS256 algorithm.

## Password security

User passwords are hashed using Argon2 through `pwdlib`.

Plain-text passwords are not stored in the Control Database.

## Authorization and roles

The platform implements role-based access control (RBAC) with three roles:

- **Admin:** administrative access, including user management and database operations.
- **User:** authenticated access to permitted database operations, including table creation.
- **Viewer:** read-only access.

User creation and listing are restricted to administrators.

Database access also considers ownership and authorization rules.

## Secrets management

Sensitive configuration is kept outside the application source code.

- **Docker Compose:** environment variables and credentials are loaded from an `.env` file, which is excluded from Git.
- **Kubernetes:** sensitive configuration is provided through Kubernetes Secrets.

Secrets must never be committed to the repository or exposed in logs.

## API protection

- Protected endpoints require JWT authentication.
- Authorization checks enforce role and ownership restrictions.
- Database identifiers are safely constructed using `psycopg.sql.Identifier` to avoid SQL injection through database names.
- Credentials and authentication tokens must not be included in application logs.

## Current limitations

The project is a prototype and requires additional hardening before production use.

Planned improvements:

- Internal TLS communication between services.
- Database sharing and more granular permissions.
- PostgreSQL Row-Level Security (RLS).
- Stronger secrets management and access policies.
- Review of Kubernetes Secret encryption, RBAC and access restrictions.
- Protection of the Prometheus metrics endpoint.
- Token expiration and rotation policy review.