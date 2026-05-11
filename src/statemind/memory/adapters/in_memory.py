from typing import Optional,List, Dict
from statemind.memory.base import BaseMemoryAdapter
from statemind.schema.models import Message


class InMemoryAdapter(BaseMemoryAdapter):
    """
    A light weight, zero dependency memory adapter
    NOTE: All data is lost when the server restarts
    """

    def __init__(self):
        self.store:Dict[str,Dict[str,List[Message]]] = {}


    def _get_key(self,user_id:Optional[str]= None, session_id:Optional[str]=None)->str:
        """Helper to create a unique dictionary key for a specific user/session"""
        return f"user:{user_id}|session:{session_id}"
    
    async def get_messages(
            self,
            tenant_id:str,
            user_id:Optional[str]= None,
            session_id:Optional[str]= None,
            limit:int=50) ->List[Message]:
        self._validate_identifiers(user_id,session_id)
        key = self._get_key(user_id,session_id)

        if tenant_id not in self.store or key not in self.store[tenant_id]:
            return []
        
        return self.store[tenant_id][key][-limit:]
    
    async def append_message(
            self,
            tenant_id:str,
            message:Message,
            user_id:Optional[str] = None,
            session_id:Optional[str] = None
    )->None:
        self._validate_identifiers(user_id,session_id)
        key = self._get_key(user_id,session_id)

        if tenant_id not in self.store:
            self.store[tenant_id] = {}

        if key not in self.store[tenant_id]:
            self.store[tenant_id][key] = []

        self.store[tenant_id][key].append(message)



    async def clear_session(self,
                            tenant_id:str,
                            user_id:Optional[str] = None,
                            session_id:Optional[str] = None)->None:
        
        self._validate_identifiers(user_id,session_id)
        key = self._get_key(user_id,session_id)

        if tenant_id in self.store and key in self.store[tenant_id]:
            del self.store[tenant_id][key]

