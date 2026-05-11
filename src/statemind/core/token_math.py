from typing import List

import tiktoken # type: ignore

from statemind.schema.models import Message


def count_tokens(text:str,model:str='gpt-4o')->int:
    """counts the number of tokens in a given string"""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


def count_message_token(messages:List[Message], model:str='gpt-4o')->int:
    """Calculates the total token count for a list of Statemind Message Objects""" 

    total_tokens = 0
    for msg in messages:
        total_tokens +=4
        total_tokens += count_tokens(msg.role,model)
        total_tokens += count_message_token(msg.content,model)

    total_tokens +=3    
    return total_tokens