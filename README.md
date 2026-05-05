# 🧠 Statemind

**Stateful AI conversations on stateless infrastructure.**

Statemind is a lightweight Python package that provides **memory, context management, and multi-tenant conversation state** for LLM applications running on **stateless servers**.

Build scalable ChatGPT-like systems **without sockets, sessions, or long-running workers**.

---

## 🚀 Why Statemind?

LLMs are stateless:
tokens in → tokens out

But users expect **stateful conversations**.

Most chatbot systems solve this using:
- WebSockets
- Sticky sessions
- Long-running threads
- In-memory state

These approaches **do not scale**.

Statemind solves this by externalizing memory and reconstructing conversational state **on every request**.

✅ Stateless servers  
✅ Horizontal scaling  
✅ Multi-tenancy support  
✅ Serverless compatible  
✅ Production-ready memory architecture  

---

## ✨ Core Idea

Statemind turns this:
Stateful chatbot server ❌

into:
Stateless API + External Memory + Context Builder ✅

Every request becomes:

1. Load memory
2. Build context
3. Call LLM
4. Save response
5. Return reply

No sessions required.

---

## 🏗 Architecture

Client
↓
Stateless API
↓
Statemind Memory Engine
↓
Context Builder
↓
LLM Provider


Statemind acts as the **Conversation State Manager** for LLM systems.

---

## 🔥 Features

### 🧠 Conversational Memory
- Short-term conversation history
- Long-term user memory
- Automatic history reconstruction

---

### 🏢 Multi-Tenant Ready
Built for SaaS platforms.

Hierarchy:
Tenant → User → Conversation → Messages

Guaranteed isolation between tenants.

---

### ⚡ Stateless by Design
Works with:

- FastAPI
- Flask
- Serverless (AWS Lambda / Cloud Run)
- Kubernetes microservices

No sockets. No sticky sessions.

---

### 🧩 Pluggable Memory Backends

- Redis
- PostgreSQL
- SQLite
- Vector databases
- Custom adapters

---

### 🪄 Context Builder (Core Feature)

Automatically:

- retrieves relevant history
- compresses old messages
- enforces token budgets
- injects system memory
- prepares model-ready prompts

---

### 🔒 Concurrency Safe
Designed for high-scale environments:

- async safe writes
- append-only conversations
- race-condition protection

---

### 🤖 Model Agnostic

Works with:

- OpenAI APIs
- local models
- vLLM
- Ollama
- HuggingFace endpoints
- custom inference servers

---

## 📦 Installation

```bash
pip install statemind

```

🎯 Design Principles
Stateless first
Infrastructure over framework
Model independence
Horizontal scalability
Minimal developer friction

Statemind is not a chatbot framework.

It is LLM state infrastructure.



















