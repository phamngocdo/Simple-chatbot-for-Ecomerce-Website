import traceback
from uuid import uuid4
from datetime import datetime
from utils.security import decode_token
from config.db_config import mongo_db as db

class ChatService:

    @staticmethod
    async def get_conversations(token: str) -> dict:
        try:
            user_id = decode_token(token).get("sub")
            data = await db["chat_data"].find_one(
                {"user_id": str(user_id)},
                {
                    "_id": 0,
                    "user_id": 1,
                    "conversations.id": 1,
                    "conversations.name":1,
                    "conversations.created_at": 1,
                    "conversations.updated_at": 1
                }
            )
            if data:
                return {
                    "user_id": data["user_id"],
                    "conversations": data["conversations"]
                }
            else:
                return {"user_id": user_id, "conversations": []}
        except Exception as e:
            traceback.print_exc()
            raise
    
    @staticmethod
    async def get_messages_from_conversation(token: str, conversation_id: str) -> dict:
        try:
            user_id = decode_token(token).get("sub")

            data = await db["chat_data"].find_one(
                {
                    "user_id": str(user_id),
                    "conversations.id": conversation_id
                },
                {
                    "_id": 0,
                    "conversations.$": 1
                }
            )
            if data and "conversations" in data:
                return data["conversations"][0]
            else:
                return {}
        except Exception as e:
            traceback.print_exc()
            raise



    @staticmethod
    async def create_new_conversation(token: str, name):
        try:
            user_id = decode_token(token).get("sub")
            new_conv = {
                "id": str(uuid4()),
                "name": name,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "messages": []
            }
            await db["chat_data"].update_one(
                {"user_id": user_id},
                {"$push": {"conversations" : new_conv}},
                update=True
            )
        except Exception as e:
            traceback.print_exc()
            raise


    @staticmethod
    async def save_chat_data(user_id: str, chat_data: dict) -> bool:
        pass


    @staticmethod
    async def get_response(user_id: str, message: str) -> str:
        pass
