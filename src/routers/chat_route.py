from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from services.chat_service import ChatService
from schemas.chat_schemas import ConversationUpdate, ConversationCreate, Message

chat_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@chat_router.get("/")
async def get_conversation(token: str = Depends(oauth2_scheme)):
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
    

@chat_router.post("/")
async def get_response_from_chatbot(message: Message, token: str = Depends(oauth2_scheme)):
    pass
    

@chat_router.post("/conversations")
async def create_new_conversation(conv: ConversationCreate, token: str = Depends(oauth2_scheme)):
    try:
        name = conv.name
        await ChatService.create_new_conversation(token=token, name=name)
        return JSONResponse(status_code=200, content={"message": "Create new conversation successful"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@chat_router.put("/conversations")
async def update_conversations(conv: ConversationUpdate, token: str = Depends(oauth2_scheme)):
    try:
        update_data = {}

        if conv.id:
            update_data["id"] = conv.id

        if conv.name:
            update_data["name"] = conv.name

        if conv.messages is not None:
            update_data["messages"] = [msg.model_dump() for msg in conv.messages]

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid data to update")

        await ChatService.save_chat_data(token=token, chat_data=update_data)
        
        return JSONResponse(status_code=200, content={"message": "Conversation updated successfully"})

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

