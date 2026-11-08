
# Mini DBaaS - API Specification

## 1. Overview

REST API for requesting and managing PostgreSQL databases.

Base path: `/api/v1`

## 2. Authentication

All endpoints require authentication.

The API identifies the requesting user and checks resource ownership before allowing operations.

## 3. Endpoints

### POST /databases

Request a new PostgreSQL database.

Request body:

```json
{
  "name": "project_alpha",
  "engine": "postgresql",
  "version": "16",
  "resources": {
    "storage_mb": 1024,
    "max_connections": 20
  }
}
```

Success response: `202 Accepted`

```json
{
  "id": "db-001",
  "name": "project_alpha",
  "status": "REQUESTED"
}
```

### GET /databases

List databases owned by the authenticated user.

Success response: `200 OK`

### GET /databases/{database_id}

Retrieve database details and provisioning status.

Success response: `200 OK`

### DELETE /databases/{database_id}

Request database deletion.

Success response: `202 Accepted`

## 4. Database states

- REQUESTED
- PROVISIONING
- READY
- FAILED
- DELETING
- DELETED

## 5. Error responses

- `400 Bad Request`: Invalid request.
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Database does not exist or is not accessible.
- `409 Conflict`: Resource conflict.
- `500 Internal Server Error`: Unexpected platform error.

## 6. Provisioning behavior

Database creation and deletion are asynchronous operations.

The API returns an operation identifier and the current resource status without waiting for provisioning to finish.

## 7. Security

- Never expose control database credentials.
- Do not return database passwords in ordinary status responses.
- Enforce resource ownership.
- Apply least-privilege access to managed databases.
