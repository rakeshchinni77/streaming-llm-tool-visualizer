from typing import Any

from pydantic import BaseModel


class TestMessageRequest(BaseModel):
    message: str


class TestMessageResponse(BaseModel):
    message: str
    response: str


class ChatStreamRequest(BaseModel):
    messages: list[Any] = []
