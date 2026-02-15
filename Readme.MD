# MCP Agent Platform

## Overview

A production‑ready AI agent backend implementing Model Context Protocol (MCP)‑style tool orchestration with multi‑LLM routing, session memory, structured logging, and containerized deployment. The system is designed to remain vendor‑agnostic while supporting reliable AI automation workflows.

---

## Key Features

* MCP‑style tool registry and execution engine
* Multi‑LLM routing (Groq primary, Gemini fallback)
* Session‑based conversational memory
* Structured logging with persistent log files
* Dockerized deployment for portability
* Vendor‑neutral AI architecture

---

## Architecture Overview

User Request → Agent Orchestrator → LLM Router (Groq/Gemini) → Tool Execution Layer → Context Memory + Logs

This layered architecture ensures reliability, observability, and provider flexibility.

---

## Tech Stack

* Python (FastAPI backend)
* Docker containerization
* Groq LLM API
* Google Gemini API
* HTTPX for async API calls
* Python logging framework

---

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/Yashkashte5/MCP-Agent
cd MCP-Agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=
GEMINI_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_MODEL=gemini-2.5-flash-lite
LLM_PROVIDER=groq
```

### 4. Run Server

```bash
uvicorn app.main:app --reload
```

Open Swagger docs:

```
http://localhost:8000/docs
```

---

## Docker Deployment

### Build Image

```bash
docker build -t mcp-agent .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env mcp-agent
```

---

## Example API Call

**Endpoint:**

```
POST /agent/run
```

**Request:**

```json
{
  "prompt": "Explain MCP",
  "session_id": "demo"
}
```

---

## Project Goals

* Reliable AI agent orchestration
* Vendor‑agnostic LLM infrastructure
* Production‑grade logging and deployment
* Expandable business automation platform

---

## Planned Improvements

* Communication integrations (Twilio, email automation)
* Multi‑agent specialization
* Vector database memory
* Monitoring dashboard
* Public cloud deployment optimization

---

## Author

**Yash Kashte**

GitHub: [https://github.com/yashkashte5](https://github.com/yashkashte5)

LinkedIn: [https://www.linkedin.com/in/yash-kashte/](https://www.linkedin.com/in/yash-kashte/)

---


