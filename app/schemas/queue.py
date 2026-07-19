from pydantic import BaseModel


class CancelVisitRequest(BaseModel):
    reason: str


class MessageResponse(BaseModel):
    message: str