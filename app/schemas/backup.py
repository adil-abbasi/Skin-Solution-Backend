from pydantic import BaseModel


class BackupResponse(BaseModel):
    message: str
    filename: str


class RestoreRequest(BaseModel):
    filename: str


class MessageResponse(BaseModel):
    message: str