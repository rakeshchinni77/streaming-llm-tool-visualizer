import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.messages import TestMessageRequest, TestMessageResponse, ChatStreamRequest
from app.services.groq_client import GroqService
from app.utils.sse import format_sse_event

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/test", response_model=TestMessageResponse)
async def chat_test(request: TestMessageRequest) -> TestMessageResponse:
    try:
        groq_service = GroqService()
        assistant_text = groq_service.generate_response(request.message)
        return TestMessageResponse(message="Groq Connected", response=assistant_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def event_generator(messages: list):
    """Generate SSE events by streaming from Groq.
    
    Args:
        messages: List of message dicts to send to Groq
    
    Yields:
        SSE-formatted event strings
    """
    try:
        groq_service = GroqService()
        for token in groq_service.stream_response(messages):
            yield format_sse_event("text_delta", {"delta": token})
    except Exception as exc:
        logger.error("SSE event generation failed: %s", exc)
        yield format_sse_event("error", {"message": str(exc)})


@router.post("/stream")
async def chat_stream(request: ChatStreamRequest) -> StreamingResponse:
    """Stream chat responses using Server-Sent Events.
    
    Receives a list of messages and streams Groq's response token-by-token.
    """
    return StreamingResponse(
        event_generator(request.messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
