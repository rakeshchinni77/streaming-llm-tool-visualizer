import json
import logging

from fastapi import APIRouter, HTTPException

from app.schemas.messages import ConversationSummaryRequest, ConversationSummaryResponse
from app.services.groq_client import GroqError, GroqRateLimitError, GroqService

logger = logging.getLogger(__name__)
router = APIRouter()


def _build_summary_prompt(messages: list) -> str:
    lines = []
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        if isinstance(content, dict):
            content = json.dumps(content, separators=(",", ":"))
        elif content is None:
            content = ""
        lines.append(f"{role.capitalize()}: {content}")

    conversation_text = "\n".join(lines)
    return (
        "Summarize the conversation below in concise plain text under 200 words. "
        "Preserve important facts and tool outputs, remove repetition, and return only the summary text.\n\n"
        f"{conversation_text}\n\nSummary:"
    )


@router.post("/summarize", response_model=ConversationSummaryResponse)
async def summarize_conversation(request: ConversationSummaryRequest) -> ConversationSummaryResponse:
    try:
        groq_service = GroqService()
        prompt = _build_summary_prompt(request.messages)
        summary = groq_service.generate_response(prompt)
        return ConversationSummaryResponse(summary=summary.strip())
    except GroqRateLimitError as exc:
        logger.warning("Groq rate limit on /summarize: %s", exc)
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again shortly.") from exc
    except GroqError as exc:
        logger.warning("Groq error on /summarize: %s", exc)
        raise HTTPException(status_code=503, detail="Unable to contact language model.") from exc
    except Exception:
        logger.exception("Summarization failed")
        raise HTTPException(status_code=500, detail="Summarization failed")
