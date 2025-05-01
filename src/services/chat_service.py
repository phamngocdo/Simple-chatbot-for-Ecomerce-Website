import traceback

from config.db_config import mongo_db as db

class ChatService:

    @staticmethod
    async def get_conversations_from_user(user_id: int) -> dict:
        try:
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
    async def get_messages_from_conversation(conversation_id: str) -> dict:
        try:
            data = await db["chat_data"].find_one(
                {"conversations.id": conversation_id},
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
            print(e)
            raise

    @staticmethod
    async def update_conversation(conversation_id: str, data: dict) -> bool:
        try:
            update_data = {}
            if "name" in data:
                update_data["conversations.$.name"] = data["name"]
            if "messages" in data:
                update_data["conversations.$.messages"] = data["messages"]
            if "updated_at" in data:
                update_data["conversations.$.updated_at"] = data["updated_at"]

            if update_data:
                result = await db["chat_data"].update_one(
                    {"conversations.id": conversation_id},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            else:
                return False
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def save_chat_data(user_id: str, chat_data: dict) -> bool:
        pass

    @staticmethod
    def get_response(user_id: str, message: str) -> str:
        pass
