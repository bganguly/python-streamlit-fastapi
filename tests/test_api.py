from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_indicators() -> None:
    response = client.get("/api/indicators")
    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload
    assert payload["items"][0]["id"] == "SE.XPD.TOTL.GD.ZS"
