import pytest #type:ignore
from statemind import Statemind,InMemoryAdapter,Message,Role


@pytest.mark.asyncio
async def test_sliding_window_drops_old_messages():
    db = InMemoryAdapter()
    engine = Statemind(memory=db)

    tenant_id = "test_org"
    user_id = "user_123"

    for i in range(5):
        msg = Message(role=Role.USER, content=f"This is a test Message. Message number {i}")
        await engine.add_message(tenant_id=tenant_id,user_id=user_id,message=msg)

    context = await engine.get_context(
            tenant_id= tenant_id,
            user_id=user_id,
            system_prompt="You are a helpful bot.",
            max_tokens = 30
        )
    
    assert context.messages[0].role == Role.SYSTEM

    assert len(context.messages) < 6

    assert context.total_tokens <= 30

    assert "number 4" in context.messages[-1].content

