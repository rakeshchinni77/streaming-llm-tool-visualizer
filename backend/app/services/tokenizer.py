import json
import os

try:
    import tiktoken
except ImportError:  # pragma: no cover
    tiktoken = None


def _get_encoding():
    if tiktoken is None:
        return None

    model = os.getenv("LLM_MODEL") or os.getenv("MODEL_NAME")

    if model:
        try:
            return tiktoken.encoding_for_model(model)
        except Exception:
            pass

    try:
        return tiktoken.get_encoding("cl100k_base")
    except Exception:
        return None


def count_tokens(messages: list) -> int:
    """Count tokens for a list of chat messages."""
    encoding = _get_encoding()
    total_tokens = 0

    if encoding:
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            total_tokens += len(encoding.encode(str(role)))
            if isinstance(content, str):
                total_tokens += len(encoding.encode(content))
            elif isinstance(content, dict):
                total_tokens += len(encoding.encode(json.dumps(content, separators=(",", ":"))))
            else:
                total_tokens += len(encoding.encode(str(content)))
    else:
        for msg in messages:
            role = str(msg.get("role", ""))
            content = msg.get("content", "")
            total_tokens += len(role.split())
            if isinstance(content, str):
                total_tokens += len(content.split())
            elif isinstance(content, dict):
                total_tokens += len(json.dumps(content, separators=(",", ":")).split())
            else:
                total_tokens += len(str(content).split())

    return total_tokens
