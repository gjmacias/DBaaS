# API Documentation

## Overview

The Mini DBaaS API is built with FastAPI and exposes REST endpoints to manage databases and platform users.

Interactive API documentation is available through Swagger UI at:

`/docs`

API routes are grouped under `/api/v1`, except health and monitoring endpoints.

## Authentication

The API uses JWT Bearer authentication.

Protected endpoints require a valid access token in the `Authorization` header:

`Authorization: Bearer <access_token>`

Users must authenticate before accessing protected resources.

## Roles and permissions

The platform currently defines three roles:

| Role | Permissions |
|---|---|
| `admin` | Full database CRUD operations, user creation and listing, table creation and read access. |
| `user` | Database operations according to ownership and authorization rules, table creation and read access. |
| `viewer` | Read-only access to databases and their data. |

User management is restricted to administrators.

## Available endpoints

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Authenticate and obtain a JWT token. | No |

### Databases

The API supports CRUD operations for database resources.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/databases` | Create and provision a database. |
| GET | `/api/v1/databases` | List registered databases. |
| GET | `/api/v1/databases/{database_id}` | Retrieve database details. |
| DELETE | `/api/v1/databases/{database_id}` | Delete a database. |

All database endpoints require authentication and enforce role and ownership permissions.

### Users

User management is currently limited to administrators.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/users` | Create a user. |
| GET | `/api/v1/users` | List users. |

### Health and monitoring

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check whether the API process is running. |
| GET | `/ready` | Check whether the Control DB is reachable. |
| GET | `/metrics` | Expose Prometheus metrics. |

## Current limitations and future work

- Database sharing between users is not implemented yet.
- Row-Level Security (RLS) is planned for more granular data access.
- MCP integration is a future improvement.
- User management currently supports creation and listing only.
- Table creation and data access are application-level capabilities, not a dedicated table-management API in the current documented scope.