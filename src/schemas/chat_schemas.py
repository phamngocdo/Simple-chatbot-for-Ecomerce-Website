from pydantic import BaseModel
from datetime import datetime
from typing import List, Literal

class Message(BaseModel):
    role: Literal["user", "bot"]
    content: str

class Conversation(BaseModel):
    id: str
    name: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime

class ConversationCreate(BaseModel):
    name: str

class ChatData(BaseModel):
    id: str
    user_id: str
    conversations: List[Conversation]