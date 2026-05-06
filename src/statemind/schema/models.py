from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Role(str,Enum):
    '''The role of the message author.'''

    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = "system"


class Message(BaseModel):
    ''' A single message in a conversation'''
    role: Role
    content: str
    token_count: Optional[int] = Field(
        default = None,
        description = "The number of tokens in this message. Calculated automatically if None"
    )


class ConversationContext(BaseModel):
    '''The final payload that the Builder prepares for the LLM'''
    messages: List[Message]
    system_prompt: Optional[str] = Field(
        default = None,
        descriptions = "The system instruction prepended to the conversation."
    )
    total_tokens: Optional[int] = Field(
        default = None,
        description = "Total tokens consumed by this context window"
    )
