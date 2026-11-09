from fastapi.testclient import TestClient

from app.main import app


# No usamos el context manager para no ejecutar el lifespan
# ni inicializar las bases de datos durante este test.
client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "mini-dbaas-api",
    }