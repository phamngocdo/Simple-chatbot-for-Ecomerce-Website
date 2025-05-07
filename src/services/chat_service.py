import traceback
from uuid import uuid4
from jwt import InvalidTokenError, ExpiredSignatureError
from datetime import datetime
from chat_model.model.llm_chatbot import LlmChatBot
from utils.security import decode_token
from config.db_config import mongo_db as db
import asyncio

import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

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
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise
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
                    "conversations": {
                        "$elemMatch": {"id": conversation_id}
                    }
                }
            )

            if data and "conversations" in data and len(data["conversations"]) > 0:
                return data["conversations"][0]
            return None
            
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise
        except Exception as e:
            traceback.print_exc()
            raise


    @staticmethod
    async def create_new_conversation(token: str, name):
        try:
            user_id = decode_token(token).get("sub")
            conv_id = str(uuid4())
            new_conv = {
                "id": conv_id,
                "name": name,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "messages": []
            }
            await db["chat_data"].update_one(
                {"user_id": user_id},
                {"$push": {"conversations" : new_conv}},
                upsert=True
            )

            return conv_id
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise
        except Exception as e:
            traceback.print_exc()
            raise

    @staticmethod
    async def save_chat_data(token: str, chat_data: dict):
        try:
            conv_id = chat_data.get("id", None)
            name = chat_data.get("name")
            messages = chat_data.get("messages", [])
            user_id = decode_token(token).get("sub")

            if not conv_id:
                conv_id = await ChatService.create_new_conversation(token, "New Conversation")

            update_data = {}

            if messages:
                update_data["$push"] = {
                    "conversations.$.messages": {
                        "$each": messages
                    }
                }

            update_data["$set"] = {
                "conversations.$.updated_at": datetime.now()
            }

            if name:
                update_data["$set"]["conversations.$.name"] = name

            await db["chat_data"].update_one(
                {
                    "user_id": str(user_id),
                    "conversations.id": conv_id
                },
                update_data
            )

            updated_data = await db["chat_data"].find_one(
                {
                    "user_id": str(user_id),
                    "conversations.id": conv_id
                },
                {
                    "_id": 0,
                    "user_id": 1,
                    "conversations": {
                        "$elemMatch": {
                            "id": conv_id
                        }
                    }
                }
            )
            if updated_data and "conversations" in updated_data:
                return updated_data["conversations"][0]

        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise
        except Exception as e:
            traceback.print_exc()
            raise


    @staticmethod
    async def delete_conversation(token: str, conversation_id: str):
        try:
            user_id = decode_token(token).get("sub")

            await db["chat_data"].update_one(
                {"user_id": user_id},
                {
                    "$pull": {
                        "conversations": {"id" :conversation_id}
                    }
                }
            )
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise
        except Exception as e:
            traceback.print_exc()
            raise


    @staticmethod
    async def get_response(token: str, message: str, old_message: dict, timeout = 30) -> str:
        try:
            user_id = str(decode_token(token).get("sub"))
            llm_chat = LlmChatBot()
            
            if not old_message:
                print("Loading")
                llm_chat.load_old_conversation_to_memory(user_id=user_id, messages=old_message)
                print("Loading done")
            
            task = asyncio.create_task(
                asyncio.to_thread(llm_chat.get_response, user_id=user_id, user_input=message)
            )
            
            try:
                return await asyncio.wait_for(task, timeout=timeout)
            except asyncio.TimeoutError:
                task.cancel() 
                raise TimeoutError(f"LLM response timed out after {timeout} seconds")
                
        except Exception as e:
            traceback.print_exc()
            raise
        



