from abc import ABC, abstractmethod
from typing import List, Optional

from statemind.schema.models import Message


class BaseMemoryAdapter(ABC):
    """
    The abtract base class for all Statemind mempory adapters.
    """

    def _validate_identifiers(self,user_id:Optional[str], session_id:Optional[str])->None:
        if not user_id and not session_id:
            raise ValueError("You must provide either a user_id or a session_id (or both) to manage state")

    @abstractmethod
    async def get_messages(
        self,
        tenant_id:str,
        message_id:Message,
        user_id: Optional[str] = None,
        session_id:Optional[str] = None,
        limit:int = 50
        ) -> List[Message]:
        """Fetch the most recent messages for a user or session"""

        pass


    @abstractmethod
    async def append_message(
        self,
        tenant_id:str,
        message: Message,
        user_id: Optional[str] = None,
        session_id:Optional[str] = None
    ) -> None:
        """saves a new single message to the database"""


    @abstractmethod
    async def clear_session(
        self,
        tenant_id:str,
        user_id:Optional[str] = None,
        session_id:Optional[str] = None
    ) ->None:
        """Delete all messages associated with a specific user or session"""
        pass


