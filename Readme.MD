# MCP Agent Platform

Production-oriented AI agent backend implementing MCP-style tool orchestration, multi-LLM routing, conversational memory, planning capability, and containerized deployment.

Designed to stay vendor-agnostic while supporting scalable AI automation workflows.

---

## 🔗 Live Demo

API Documentation:

[https://mcp-agent-85o5.onrender.com/docs](https://mcp-agent-85o5.onrender.com/docs)

Example endpoint:

POST `/agent/run`

---

##  Overview

This project provides a backend platform for building AI agents that can:

* Route prompts across multiple LLM providers
* Execute external tools deterministically
* Maintain session memory
* Plan multi-step actions
* Integrate with communication systems
* Run reliably in production environments

It follows an MCP-inspired architecture emphasizing modularity, observability, and provider independence.

---

##  Key Features

### Core Agent Capabilities

* MCP-style tool registry and execution engine
* Reactive tool-calling agent loop
* Planner layer for multi-step reasoning
* JSON guardrails for structured LLM responses

### LLM Infrastructure

* Multi-LLM routing:

  * Groq (primary inference)
  * Gemini (fallback)
* Vendor-neutral architecture

### Memory & Context

* Session-based conversational memory
* Automatic conversation summarization
* Context persistence across requests

### Integration Layer

* Twilio webhook groundwork for telephony automation
* API-first architecture for external integrations

### Production Readiness

* Structured logging
* Docker containerization
* Render cloud deployment tested
* Async-first FastAPI backend

---

##  Architecture Overview

```
User Request
     ↓
Agent Orchestrator
     ↓
Planner Layer (optional)
     ↓
LLM Router
(Groq Primary → Gemini Fallback)
     ↓
Tool Execution Layer
     ↓
Memory + Logging + Integrations
```

This layered design ensures:

* reliability
* observability
* extensibility
* provider flexibility

---

## 🛠 Tech Stack

### Backend

* Python
* FastAPI (async API framework)
* HTTPX (async API calls)

### AI Infrastructure

* Groq LLM API
* Google Gemini API

### Deployment & Ops

* Docker containerization
* Render cloud deployment
* Python structured logging

### Integrations (In Progress)

* Twilio voice/SMS automation

---

##  Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/Yashkashte5/MCP-Agent
cd MCP-Agent
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create `.env`:

```
GROQ_API_KEY=
GEMINI_API_KEY=

GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_MODEL=gemini-2.5-flash-lite

LLM_PROVIDER=groq
```

---

### 4. Run Server

```bash
uvicorn app.main:app --reload
```

Open:

```
http://localhost:8000/docs
```

---

##  Docker Deployment

### Build Image

```bash
docker build -t mcp-agent .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env mcp-agent
```

---

##  Example API Call

**Endpoint**

```
POST /agent/run
```

**Request Body**

```json
{
  "prompt": "Explain Model Context Protocol",
  "session_id": "demo"
}
```

---

##  Project Goals

* Reliable AI agent orchestration
* Vendor-agnostic LLM infrastructure
* Real-world automation capabilities
* Production-ready deployment workflows
* Expandable AI business automation platform

---

##  Planned Improvements

### Near Term

* Full Twilio voice automation
* Email automation integration
* Improved planner validation
* Enhanced memory persistence

### Mid Term

* Multi-agent specialization
* Vector database memory
* Observability dashboard
* Tool ecosystem expansion

### Long Term

* Autonomous business automation agents
* Voice-first AI assistants
* Scalable agent orchestration platform

---

##  Author

**Yash Kashte**

GitHub:
[https://github.com/yashkashte5](https://github.com/yashkashte5)

LinkedIn:
[https://www.linkedin.com/in/yash-kashte/](https://www.linkedin.com/in/yash-kashte/)

---
