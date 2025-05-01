from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.chat_service import ChatService

chat_router = APIRouter()

#Mới chỉ có test, cần viết middleware hoặc lấy từ token
class Conversation(BaseModel):
    name: str


@chat_router.get("/users/{user_id}")
async def get_conversation(user_id: int):
    try:
        conversation = await ChatService.get_conversations_from_user(user_id)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@chat_router.get("/conversations/{conversation_id}")
async def get_messages(conversation_id: str):
    try:
        messages = await ChatService.get_messages_from_conversation(conversation_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@chat_router.put("/conversations/{conversation_id}")
async def update_conversation_name(conversation_id: str, conversation: Conversation):
    name = conversation.name
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    try:
        result = await ChatService.update_conversation(conversation_id, {"name": name})
        if result:
            return JSONResponse(status_code=200, content={"message": "Conversation updated successfully"})
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")