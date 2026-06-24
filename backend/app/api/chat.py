from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.messages import TestMessageRequest, TestMessageResponse, ChatStreamRequest
from app.services.groq_client import GroqService
from app.utils.sse import format_sse_event

router = APIRouter()


@router.post("/test", response_model=TestMessageResponse)
async def chat_test(request: TestMessageRequest) -> TestMessageResponse:
    try:
        groq_service = GroqService()
        assistant_text = groq_service.generate_response(request.message)
        return TestMessageResponse(message="Groq Connected", response=assistant_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def event_generator():
    """Generate SSE events for streaming response."""
    # Stream a single text_delta event
    yield format_sse_event("text_delta", {"delta": "Hello"})


@router.post("/stream")
async def chat_stream(request: ChatStreamRequest) -> StreamingResponse:
    """Stream chat responses using Server-Sent Events."""
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
