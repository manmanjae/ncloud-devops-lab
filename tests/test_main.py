from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_version():
    response = client.get("/version")
    body = response.json()

    assert response.status_code == 200
    assert "version" in body
    assert "hostname" in body
    assert "uptime_seconds" in body

def test_root_uses_default_message(monkeypatch):
    monkeypatch.delenv("APP_MESSAGE", raising=False)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "devops-lab-api",
        "message": "Hello from Kubernetes",
    }


def test_root_uses_environment_message(monkeypatch):
    monkeypatch.setenv("APP_MESSAGE", "Hello from ConfigMap test")

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "devops-lab-api",
        "message": "Hello from ConfigMap test",
    }
