from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from services.chat_service import ChatService
from typing import Optional
from schemas.chat_schemas import Conversation, ConversationCreate

chat_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@chat_router.get("/")
async def get_conversation(request: Request):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        conversation = await ChatService.get_conversations(token=token)
        return conversation
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    
    
@chat_router.get("/conversations/{conversation_id}")
async def get_messages(conversation_id: str, request: Request):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        messages = await ChatService.get_messages_from_conversation(token=token, conversation_id=conversation_id)
        if not messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return messages
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@chat_router.get("/response")
async def get_response_from_chatbot(message: str, request: Request, conversation_id: Optional[str] = None):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        old_messages = None
        
        if conversation_id:
            old_messages = await ChatService.get_messages_from_conversation(token, conversation_id)

        result = await ChatService.get_response(token=token, message=message, old_message=old_messages)
        return JSONResponse(status_code=200, content={"answer": result})

    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except (Exception, TimeoutError) as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@chat_router.post("/conversations")
async def create_new_conversation(conv: ConversationCreate, request: Request):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        name = conv.name
        await ChatService.create_new_conversation(token=token, name=name)
        return JSONResponse(status_code=200, content={"message": "Create new conversation successful"})
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

@chat_router.put("/conversations")
async def update_conversations(conv: Conversation, request: Request):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        update_data = {}

        if conv.id:
            update_data["id"] = conv.id

        if conv.name:
            update_data["name"] = conv.name

        if conv.messages is not None:
            update_data["messages"] = [msg.model_dump() for msg in conv.messages]

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid data to update")

        result = await ChatService.save_chat_data(token=token, chat_data=update_data)
        return result
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@chat_router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, request: Request):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        await ChatService.delete_conversation(token=token, conversation_id=conversation_id)
        return JSONResponse(status_code=200, content={"message": "Delete conversation successfully"})
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
