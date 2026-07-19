# 🚀 Production LLM & RAG API with LangChain

An enterprise-ready, high-performance production API wrapper built for LLM agents and Retrieval-Augmented Generation (RAG). Powered by **FastAPI**, **LangChain**, **Pydantic V2**, and **LangSmith** for observability, caching, and robust production-grade reliability.

---

## 🌟 Key Features

- **⚡ High-Performance Gateway**: Built on FastAPI with asynchronous routing for fast response times.
- **🧠 LangChain Agent Pipeline**: Advanced agent workflows integrating OpenAI models with automated fallback routing (`gpt-4o-mini` ➔ `gpt-5-mini` / fallbacks).
- **🕵️ LangSmith Observability**: Built-in production tracing, evaluation, and logging out-of-the-box.
- **🛡️ Production-Grade Security**: Rate limiting, API key validation, and request sanitization.
- **💾 Smart Caching Layer**: Configurable cache TTL to reduce redundant LLM calls and control costs.
- **📊 Real-time Metrics & Health Checks**: Track latency, cache hit rate, token counts, and system environment status.
- **⚙️ Centralized Settings Management**: Environment validation using `pydantic-settings` to avoid missing configuration errors at startup.

---

## 🛠️ Project Structure

```text
production-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── agent.py         # LangChain Agent and RAG logic
│   ├── cache.py         # Memory/Redis caching mechanism
│   ├── config.py        # Validated configuration settings via Pydantic
│   ├── models.py        # Pydantic schemas for requests and responses
│   ├── monitering.py    # Health & latency metrics instrumentation
│   └── security.py      # Rate limiter & API security utilities
├── tests/               # Unit and integration tests
├── .env                 # Environment variables (secrets)
├── pyproject.toml       # Dependencies managed with uv
├── test.py              # Configuration self-test script
└── README.md            # You are here!
```

---

## 🚀 Getting Started

### 📋 Prerequisites

- **Python**: `>= 3.12`
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mekin-jema/Production-RAG-with-Langchain.git
   cd Production-RAG-with-Langchain
   ```

2. **Setup Virtual Environment & Install Dependencies**:
   ```bash
   uv sync
   ```
   *This automatically creates a `.venv` and installs all dependencies specified in `pyproject.toml`.*

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   # LLM Credentials
   OPENAI_API_KEY=your_openai_api_key_here
   PRIMARY_MODEL=gpt-4o-mini
   FALLBACK_MODEL=gpt-4o

   # LangSmith Monitoring (Optional but recommended)
   LANGSMITH_TRACING_V2=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_PROJECT=production-api

   # App Settings
   APP_ENV=development
   LOG_LEVEL=INFO
   RATE_LIMIT=20/min
   CACHE_TTL_SECONDS=300
   MAX_RETRIES=3
   ```

4. **Verify Configuration**:
   ```bash
   uv run python test.py
   ```

---

## 🏃 Running the Application

Start the FastAPI development server using `uv`:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive Swagger UI documentation is served at `http://127.0.0.1:8000/docs`.

---

## 📡 API Endpoints Reference

### 1. Chat Completion / Agent Execution
* **Endpoint**: `POST /api/v1/chat`
* **Request Body** ([ChatRequest](file:///c:/Users/Mekin.Jemal/OneDrive%20-%20Safaricom%20Ethiopia/Desktop/Projects/LLM/production-api/app/models.py#L9-L25)):
  ```json
  {
    "message": "Explain the concept of quantum computing briefly.",
    "thread_id": "session_123"
  }
  ```
* **Response Body** ([ChatResponse](file:///c:/Users/Mekin.Jemal/OneDrive%20-%20Safaricom%20Ethiopia/Desktop/Projects/LLM/production-api/app/models.py#L26-L36)):
  ```json
  {
    "response": "Quantum computing is a type of computation whose operations can harness the phenomena of quantum mechanics...",
    "thread_id": "session_123",
    "model_used": "gpt-4o-mini",
    "cached": false,
    "processing_time_ms": 342.5,
    "timestamp": "2026-07-19T17:10:00Z"
  }
  ```

### 2. System Health Status
* **Endpoint**: `GET /health`
* **Response Body** ([HealthResponse](file:///c:/Users/Mekin.Jemal/OneDrive%20-%20Safaricom%20Ethiopia/Desktop/Projects/LLM/production-api/app/models.py#L37-L43)):
  ```json
  {
    "status": "healthy",
    "environment": "development",
    "version": "1.0.0",
    "checks": {
      "openai_api": "connected",
      "cache_db": "healthy"
    }
  }
  ```

### 3. Usage Metrics
* **Endpoint**: `GET /metrics`
* **Response Body** ([MetricsResponse](file:///c:/Users/Mekin.Jemal/OneDrive%20-%20Safaricom%20Ethiopia/Desktop/Projects/LLM/production-api/app/models.py#L44-L53)):
  ```json
  {
    "total_requests": 1402,
    "total_errors": 4,
    "error_rate": "0.28%",
    "avg_latency_ms": 194.3,
    "cache_hit_rate": "34.2%",
    "total_input_tokens": 42031,
    "total_output_tokens": 150240
  }
  ```

---

## 🧪 Testing

Run unit and integration tests using `pytest`:

```bash
uv run pytest
```

---

## 📜 License

This project is licensed under the MIT License.
