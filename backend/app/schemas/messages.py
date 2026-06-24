from pydantic import BaseModel


class TestMessageRequest(BaseModel):
    message: str


class TestMessageResponse(BaseModel):
    message: str
    response: str
