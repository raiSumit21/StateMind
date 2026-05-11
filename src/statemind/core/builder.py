from typing import List, Optional

from statemind.core.token_math import count_message_token
from statemind.memory.base import BaseMemoryAdapter
from statemind.schema.models import ConversationContext, Message, Role


class Statemind:
    """
    The core engine of statemind.
    Manages conversational context, enforces token budgets, and interface with the database.
    """

    def __init__(self,memory:BaseMemoryAdapter):
        """
        Initialize Statemind with the chosen database adapter
        """
        self.memory = memory


    async def get_context(
            self,
            tenant_id:str,
            user_id:Optional[str] = None,
            session_id:Optional[str] = None,
            system_prompt: Optional[str] = None,
            max_tokens:int = 4000,
            model:str = 'gpt-4o'
    )-> ConversationContext:
        """
        Fetches conversation history  and dynamically compress it to fit within the 
        max token budget
        """
        #1. Fetch raw history from the database
        history = await self.memory.get_messages(
            tenant_id=tenant_id,
            user_id=user_id,
            session_id=session_id,
            limit=100
        )   
        #2 Prepare the System Prompt (if provided)
        final_message: List[Message] = []
        system_msg = None
        if system_prompt:
            system_msg = Message(role=Role.SYSTEM,content = system_prompt)
            final_message.append(system_msg)

        #3. The sliding window Algorithm
        while history:
            current_draft = final_message + history
            current_tokens = count_message_token(current_draft,model)

            if current_tokens <=max_tokens:
                break

            history.pop(0)

        final_message.extend(history)

        final_token_count = count_message_token(final_message,model)

        #return the perfectly assembled context

        return ConversationContext(
            messages = final_message,
            system_prompt = system_prompt,
            total_tokens = final_token_count
        )

    async def add_message(
            self,
            tenant_id:str,
            message:Message,
            user_id:Optional[str] = None,
            session_id:Optional[str] = None,
    )-> None:
        """
        Helper method to save a new message to the database
        """
        await self.memory.append_message(
            tenant_id=tenant_id,
            user_id=user_id,
            session_id=session_id,
            message=message
        )