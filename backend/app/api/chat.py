from fastapi import APIRouter, HTTPException

from app.schemas.messages import TestMessageRequest, TestMessageResponse
from app.services.groq_client import GroqService

router = APIRouter()


@router.post("/test", response_model=TestMessageResponse)
async def chat_test(request: TestMessageRequest) -> TestMessageResponse:
    try:
        groq_service = GroqService()
        assistant_text = groq_service.generate_response(request.message)
        return TestMessageResponse(message="Groq Connected", response=assistant_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
