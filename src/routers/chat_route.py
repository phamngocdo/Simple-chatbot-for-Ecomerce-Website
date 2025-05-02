from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from services.chat_service import ChatService
from schemas.chat_schemas import ChatData, Conversation, Message

chat_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Conversation(BaseModel):
    name: str


@chat_router.get("/users/{user_id}")
async def get_conversation(user_id: int, token: str = Depends(oauth2_scheme)):
    try:
        conversation = await ChatService.get_conversations(token=token)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@chat_router.get("/conversations/{conversation_id}")
async def get_messages(conversation_id: str, token: str = Depends(oauth2_scheme)):
    try:
        messages = await ChatService.get_messages_from_conversation(token=token, conversation_id=conversation_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@chat_router.put("/conversations/{conversation_id}")
async def update_conversation(conv: Conversation):
    try:
        data = {
            "id": conv.id,
            "name": conv.name
            
        }
    except Exception as e:
        raise