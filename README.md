# 🧠 Statemind

**Statemind** is a lightweight, zero-dependency Python package designed to manage **multi-tenant conversational memory** for LLM applications.

Whether you are building a serverless FastAPI backend, a Streamlit app, or running a local LLM via Ollama, **Statemind acts as the invisible brain** that manages chat history and guarantees your context never exceeds the model’s token limit.

---

## ✨ Features

- ✅ **Token-Aware Sliding Window**  
  Automatically trims old messages when history exceeds your `max_tokens` budget.

- ✅ **Multi-Tenant Ready**  
  Supports tenants → users → conversations out of the box.

- ✅ **Stateless Server Compatible**  
  Designed for serverless and horizontally scalable architectures.

- ✅ **Pluggable Storage Architecture**  
  Works with in-memory storage, MongoDB, or custom adapters.

- ✅ **Strict Data Contracts**  
  Uses Pydantic models to guarantee consistent message formatting.

- ✅ **Model Agnostic**  
  Works with OpenAI, Anthropic, HuggingFace, Ollama, or any local LLM.

---

## 📦 Installation

```bash
pip install statemind
```

For MongoDB support:

```bash
pip install statemind pymongo
```

---

## 🚀 Quick Start

Statemind separates **memory management** from **LLM inference**.

### 1️⃣ Setup the Engine

```python
from statemind import Statemind, InMemoryAdapter

db = InMemoryAdapter()
engine = Statemind(memory=db)
```

---

### 2️⃣ Chat Lifecycle

```python
import asyncio
from statemind import Message, Role

async def main():
    tenant_id = "my_startup"
    user_id = "user_123"

    # Save user message
    user_msg = Message(role=Role.USER, content="Hello! I need help with Python.")
    await engine.add_message(
        tenant_id=tenant_id,
        user_id=user_id,
        message=user_msg
    )

    # Build optimized context window
    context = await engine.get_context(
        tenant_id=tenant_id,
        user_id=user_id,
        system_prompt="You are a senior Python developer.",
        max_tokens=2000
    )

    # Call your LLM here
    ai_text = "Of course! What Python concepts are you struggling with?"

    # Save assistant response
    ai_msg = Message(role=Role.ASSISTANT, content=ai_text)
    await engine.add_message(
        tenant_id=tenant_id,
        user_id=user_id,
        message=ai_msg
    )

asyncio.run(main())
```

---

## 🧩 Architecture Philosophy

Statemind treats chat systems as:

```
Tenant → User → Session → Messages
```

Instead of keeping state in sockets or threads, Statemind:

- stores memory externally
- rebuilds context on demand
- enables massive horizontal scaling

This makes it ideal for:

- Serverless APIs
- Stateless microservices
- Multi-tenant SaaS chat platforms
- Local LLM applications

---

## 🔌 Included Adapters

### InMemoryAdapter

Best for:

- local development
- testing
- Streamlit apps

Data resets when the server restarts.

---

### MongoAdapter

Production-ready persistent storage.

```python
from statemind import MongoAdapter

db = MongoAdapter(
    uri="mongodb://localhost:27017",
    db_name="statemind_prod",
    collection_name="messages"
)
```

Supports thousands of concurrent users without blocking async workloads.

---

## 🧠 Works With Local LLMs

Statemind integrates seamlessly with:

- Ollama
- llama.cpp
- HuggingFace Transformers
- vLLM
- OpenAI-compatible APIs

You control inference.  
Statemind controls memory.

---

## 🤝 Contributing

Pull requests are welcome!

Before submitting:

```bash
ruff check .
pytest tests/
```

Please open an issue first for major feature discussions.

---

## 🌱 Development Workflow

Create documentation branch:

```bash
git checkout dev
git pull origin dev
git checkout -b docs/readme-update
```

Push updates:

```bash
git add README.md
git commit -m "docs: write comprehensive README and Quick Start guide"
git push -u origin docs/readme-update
```

Then open a Pull Request against `dev`.

---

## 📜 License

MIT License

---

## ⭐ Vision

Statemind aims to become the **standard memory layer for LLM applications**, enabling developers to build scalable conversational systems without managing state manually.

```
Stateless servers.
Stateful conversations.
```

---
