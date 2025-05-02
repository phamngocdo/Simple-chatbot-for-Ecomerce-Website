from pydantic import BaseModel
from typing import List, Optional, Literal

class Message(BaseModel):
    role: Literal["user", "chatbot"]
    content: str

class ConversationUpdate(BaseModel):
    id: Optional[str]
    name: Optional[str]
    messages: Optional[List[Message]]

class ConversationCreate(BaseModel):
    name: str
