import logging
import re
import time

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.schemas.messages import TestMessageRequest, TestMessageResponse, ChatStreamRequest
from app.services.groq_client import GroqError, GroqRateLimitError, GroqService
from app.services.tool_engine import ToolEngine
from app.services.tokenizer import count_tokens
from app.utils.sse import format_sse_event

logger = logging.getLogger(__name__)
router = APIRouter()
tool_engine = ToolEngine()

CALCULATOR_PATTERN = re.compile(r"[\d][\d\s\.\+\-\*\/\(\)]*")
CALCULATOR_OPERATOR = re.compile(r"[\+\-\*\/\(\)]")

# Time triggers (case-insensitive substrings)
TIME_TRIGGERS = ["what time is it", "current time", "utc", "time", "current utc time"]
KNOWLEDGE_TRIGGERS = ["atlas", "launch", "knowledge", "project", "tell me about"]


def detect_current_time(text: str) -> str | None:
    if not text or not isinstance(text, str):
        return None
    low = text.lower()
    for trig in TIME_TRIGGERS:
        if trig in low:
            return "UTC"
    return None


def detect_knowledge_query(text: str) -> str | None:
    if not text or not isinstance(text, str):
        return None
    low = text.lower()
    for trig in KNOWLEDGE_TRIGGERS:
        if trig in low:
            return text
    return None


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
    except GroqRateLimitError as exc:
        logger.warning("Groq rate limit on /test: %s", exc)
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again shortly.") from exc
    except GroqError as exc:
        logger.warning("Groq error on /test: %s", exc)
        raise HTTPException(status_code=503, detail="Unable to contact language model.") from exc
    except Exception as exc:
        logger.exception("Unexpected error on /test")
        raise HTTPException(status_code=500, detail="Internal server error.") from exc


async def event_generator(request: Request, messages: list):
    """Generate SSE events by streaming from Groq or running a tool request."""
    start_time = time.time_ns()
    total_tokens = count_tokens(messages)

    def _extract_text_from_message(msg: dict) -> str | None:
        content = msg.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, dict):
            # common keys that might hold text
            for k in ("text", "content", "message", "body"):
                v = content.get(k)
                if isinstance(v, str):
                    return v
        return None

    async def _generate():
        if await request.is_disconnected():
            logger.info("Client disconnected before streaming started.")
            return

        latest_user_message = None
        for message in reversed(messages):
            if await request.is_disconnected():
                logger.info("Client disconnected while scanning messages.")
                return
            if message.get("role") == "user":
                text = _extract_text_from_message(message)
                if text:
                    latest_user_message = text
                    break

        # Tool routing and execution
        knowledge_query = detect_knowledge_query(latest_user_message)
        if knowledge_query:
            tool_id = "kb-1"
            start_payload = {
                "tool": "knowledge_base",
                "id": tool_id,
                "input": {"query": knowledge_query},
            }
            yield format_sse_event("tool_call_start", start_payload)

            result_payload = tool_engine.execute("knowledge_base", {"query": knowledge_query})
            if result_payload["success"]:
                yield format_sse_event(
                    "tool_result",
                    {"id": tool_id, "result": result_payload["result"]},
                )
                yield format_sse_event("text_delta", {"delta": result_payload["result"].get("answer", "")})
            else:
                logger.warning("Tool execution failed for knowledge_base: %s", result_payload["error"])
                yield format_sse_event(
                    "tool_result",
                    {"id": tool_id, "error": "Tool execution failed."},
                )
                yield format_sse_event("text_delta", {"delta": "I could not find that information."})
            return

        tz = detect_current_time(latest_user_message)
        if tz:
            tool_id = "time-1"
            start_payload = {
                "tool": "current_time",
                "id": tool_id,
                "input": {"timezone": tz},
            }
            yield format_sse_event("tool_call_start", start_payload)

            result_payload = tool_engine.execute("current_time", {"timezone": tz})
            if result_payload["success"]:
                yield format_sse_event(
                    "tool_result",
                    {"id": tool_id, "result": result_payload["result"]},
                )
                yield format_sse_event(
                    "text_delta",
                    {"delta": f"The current UTC time is {result_payload['result'].get('current_time')}"},
                )
            else:
                logger.warning("Tool execution failed for current_time: %s", result_payload["error"])
                yield format_sse_event(
                    "tool_result",
                    {"id": tool_id, "error": "Tool execution failed."},
                )
                yield format_sse_event("text_delta", {"delta": "I could not fetch the current time."})
            return

        calculator_expression = extract_calculator_expression(latest_user_message)
        if calculator_expression:
            tool_id = "calc-1"
            start_payload = {
                "tool": "calculator",
                "id": tool_id,
                "input": {"expression": calculator_expression},
            }
            yield format_sse_event("tool_call_start", start_payload)

            result_payload = tool_engine.execute("calculator", {"expression": calculator_expression})
            if result_payload["success"]:
                yield format_sse_event(
                    "tool_result",
                    {"id": tool_id, "result": result_payload["result"]},
                )
                yield format_sse_event("text_delta", {"delta": f"The answer is {result_payload['result']}"})
            else:
                logger.warning("Tool execution failed for calculator: %s", result_payload["error"])
                yield format_sse_event(
                    "tool_result",
                    {"id": tool_id, "error": "Tool execution failed."},
                )
                yield format_sse_event("text_delta", {"delta": "I could not calculate that expression."})
            return

        try:
            groq_service = GroqService()
            for token in groq_service.stream_response(messages):
                if await request.is_disconnected():
                    logger.info("Client disconnected during Groq stream.")
                    return
                yield format_sse_event("text_delta", {"delta": token})
        except GroqRateLimitError as exc:
            logger.warning("Groq rate limit error: %s", exc)
            yield format_sse_event(
                "error",
                {"type": "rate_limit", "message": str(exc)},
            )
            return
        except GroqError as exc:
            logger.warning("Groq error: %s", exc)
            yield format_sse_event(
                "error",
                {"type": "groq_error", "message": str(exc)},
            )
            return

    try:
        async for event in _generate():
            if await request.is_disconnected():
                logger.info("Client disconnected while streaming SSE events.")
                return
            yield event
    except Exception:
        logger.exception("SSE event generation failed")
        if not await request.is_disconnected():
            yield format_sse_event(
                "error",
                {"type": "internal_error", "message": "An internal streaming error occurred."},
            )
    finally:
        if not await request.is_disconnected():
            duration_ms = round((time.time_ns() - start_time) / 1_000_000)
            yield format_sse_event(
                "done",
                {"totalTokens": total_tokens, "durationMs": duration_ms},
            )


@router.post("/stream")
async def chat_stream(request: Request, payload: ChatStreamRequest) -> StreamingResponse:
    """Stream chat responses using Server-Sent Events.
    
    Receives a list of messages and streams Groq's response token-by-token.
    """
    return StreamingResponse(
        event_generator(request, payload.messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
