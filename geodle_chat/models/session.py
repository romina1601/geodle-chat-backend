from pydantic import BaseModel

class SessionLogEntry(BaseModel):
    session_id: str
    time: str
