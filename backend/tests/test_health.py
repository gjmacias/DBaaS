from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import app
from app.api.routes import health


# No usamos el context manager para no ejecutar el lifespan
# ni inicializar las bases de datos durante estos tests.
client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "mini-dbaas-api",
    }


def test_readiness_check_success(monkeypatch):
    class FakeConnection:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

        def execute(self, query):
            return 1

    class FakeEngine:
        def connect(self):
            return FakeConnection()

    monkeypatch.setattr(health, "engine", FakeEngine())

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "control_db": "ok",
        },
    }


def test_readiness_check_database_error(monkeypatch):
    class FakeEngine:
        def connect(self):
            raise OperationalError(
                "SELECT 1",
                {},
                Exception("Database unavailable"),
            )

    monkeypatch.setattr(health, "engine", FakeEngine())

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {
            "control_db": "error",
        },
    }