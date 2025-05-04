from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from services.chat_service import ChatService
from schemas.chat_schemas import ConversationUpdate, ConversationCreate, Message

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
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@chat_router.get("/conversations/{conversation_id}")
async def get_messages(conversation_id: str, request: Request):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        messages = await ChatService.get_messages_from_conversation(token=token, conversation_id=conversation_id)
        return messages
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@chat_router.post("/")
async def get_response_from_chatbot(message: Message, request: Request):
    pass
    

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
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@chat_router.put("/conversations")
async def update_conversations(conv: ConversationUpdate, request: Request):
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

        await ChatService.save_chat_data(token=token, chat_data=update_data)
        
        return JSONResponse(status_code=200, content={"message": "Conversation updated successfully"})
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@chat_router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, request: Request):
    try:
        token = request.session.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        await ChatService.delete_conversation(token=token, conversation_id=conversation_id)
        return JSONResponse(status_code=200, content={"message": "Delete conversation successfully"})
    except (ExpiredSignatureError, InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
