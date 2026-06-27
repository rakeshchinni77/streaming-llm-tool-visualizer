from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.summarize.GroqService")
def test_summarize_endpoint_returns_summary(mock_groq_service) -> None:
    mock_groq_service.return_value.generate_response.return_value = "A concise summary"

    response = client.post(
        "/api/chat/summarize",
        json={"messages": [{"role": "user", "content": "Hello"}]},
    )

    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json()["summary"]
