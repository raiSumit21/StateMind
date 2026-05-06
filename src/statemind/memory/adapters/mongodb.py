from datetime import datetime, timezone
from typing import List, Optional

from pymongo import AsyncMongoClient

from statemind.memory.base import BaseMemoryAdapter
from statemind.schema.models import Message


class MongoAdapter(BaseMemoryAdapter):
    """
    Docstring for MongoAdapter
    """

    def __init__(self,uri:str, db_name:str= "statemind", collection_name:str="messages"):
        """
        Initialize the connection
        """

        self.client :AsyncMongoClient = AsyncMongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]


    async def get_messages(
            self,
            tenant_id:str,
            user_id:Optional[str] = None,
            session_id:Optional[str] = None,
            limit:int = 50
    )-> List[Message]:
        self._validate_identifiers(user_id,session_id)
        query = {
            "tenant_id": tenant_id
        }

        if user_id:
            query["user_id"] = user_id

        if session_id:
            query['session_id'] = session_id

        cursor = self.collection.find(query).sort("timestamp",1)
        documents = await cursor.to_list(length=limit)
        return [Message(**doc["message"]) for doc in documents]
    

    async def append_message(
            self,
            tenant_id:str,
            message:Message,
            user_id:Optional[str] = None,
            session_id:Optional[str] = None)->None:
        
        self._validate_identifiers(user_id,session_id)
        document = {
            "tenant_id": tenant_id,
            "user_id": user_id,
            "session_id":session_id,
            "message": message.model_dump(),
            "timestamp": datetime.now(timezone.utc)
        }

        await self.collection.insert_one(document)

    async def clear_session(self, tenant_id, user_id = None, session_id = None):
        self._validate_identifiers(user_id,session_id)

        query = {"tenant_id": tenant_id}
        if user_id:
            query["user_id"] = user_id

        if session_id:
            query["session_id"] = session_id

        await self.collection.delete_many(query)