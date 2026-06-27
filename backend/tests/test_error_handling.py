from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_malformed_json_returns_validation_error() -> None:
    response = client.post(
        "/api/chat/test",
        data='{"message":',
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 422


def test_unknown_route_returns_not_found() -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
