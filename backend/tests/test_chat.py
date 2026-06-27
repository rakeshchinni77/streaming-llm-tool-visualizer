from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.chat.GroqService")
def test_chat_test_endpoint_returns_connected_message(mock_groq_service) -> None:
    mock_groq_service.return_value.generate_response.return_value = "Hello from mocked Groq"

    response = client.post("/api/chat/test", json={"message": "Hello"})

    assert response.status_code == 200
    assert response.json()["message"] == "Groq Connected"
