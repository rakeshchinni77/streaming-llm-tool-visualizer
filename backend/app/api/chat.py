import logging
import re
import time

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.messages import TestMessageRequest, TestMessageResponse, ChatStreamRequest
from app.services.groq_client import GroqService
from app.services.tool_engine import ToolEngine
from app.utils.sse import format_sse_event

logger = logging.getLogger(__name__)
router = APIRouter()

CALCULATOR_PATTERN = re.compile(r"[\d][\d\s\.\+\-\*\/\(\)]*")
CALCULATOR_OPERATOR = re.compile(r"[\+\-\*\/\(\)]")

def extract_calculator_expression(text: str) -> str | None:
    if not text or not isinstance(text, str):
        return None

    match = CALCULATOR_PATTERN.search(text)
    if not match:
        return None

    expression = match.group(0).strip()
    if not CALCULATOR_OPERATOR.search(expression):
        return None

    return expression


@router.post("/test", response_model=TestMessageResponse)
async def chat_test(request: TestMessageRequest) -> TestMessageResponse:
    try:
        groq_service = GroqService()
        assistant_text = groq_service.generate_response(request.message)
        return TestMessageResponse(message="Groq Connected", response=assistant_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def event_generator(messages: list):
    """Generate SSE events by streaming from Groq or running a tool request."""
    latest_user_message = None
    for message in reversed(messages):
        if message.get("role") == "user" and isinstance(message.get("content"), str):
            latest_user_message = message.get("content")
            break

    calculator_expression = extract_calculator_expression(latest_user_message)
    if calculator_expression:
        tool_engine = ToolEngine()
        tool_id = "calc-1"
        start_payload = {
            "tool": "calculator",
            "id": tool_id,
            "input": {"expression": calculator_expression},
        }
        yield format_sse_event("tool_call_start", start_payload)

        try:
            start = time.perf_counter()
            result = tool_engine.execute_tool("calculator", {"expression": calculator_expression})
            duration_ms = int((time.perf_counter() - start) * 1000)
            yield format_sse_event(
                "tool_result",
                {"id": tool_id, "result": result, "durationMs": duration_ms},
            )
            yield format_sse_event("text_delta", {"delta": f"The answer is {result}"})
            return
        except Exception as exc:
            logger.error("Calculator tool failed: %s", exc)
            yield format_sse_event("text_delta", {"delta": "I could not calculate that expression."})
            return

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
