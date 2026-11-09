from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_databases_without_token():
    response = client.get("/api/v1/databases")

    assert response.status_code == 401


def test_list_databases_with_invalid_token():
    response = client.get(
        "/api/v1/databases",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


def test_login_without_required_fields():
    response = client.post(
        "/api/v1/auth/login",
        json={},
    )

    assert response.status_code == 422