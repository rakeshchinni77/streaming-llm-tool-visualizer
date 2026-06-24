import json


def format_sse_event(event_name: str, payload: dict) -> str:
    """Format a Server-Sent Events message with event name and payload.
    
    Args:
        event_name: The SSE event type (e.g., 'text_delta')
        payload: Dictionary to serialize as JSON in the data field
    
    Returns:
        Formatted SSE message with two trailing newlines
    """
    data_str = json.dumps(payload)
    return f"event: {event_name}\ndata: {data_str}\n\n"
