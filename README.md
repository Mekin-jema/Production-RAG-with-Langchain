# Production LLM and RAG API with LangChain

An enterprise-ready production API wrapper built for LLM agents and Retrieval-Augmented Generation (RAG). Powered by FastAPI, LangChain, Pydantic V2, and LangSmith for observability, caching, and production-grade reliability.

---

## Key Features

- High-performance gateway built on FastAPI with asynchronous routing for fast response times.
- LangChain agent pipeline with OpenAI models and automated fallback routing.
- LangSmith observability with tracing, evaluation, and logging.
- Production-grade security with rate limiting, API key validation, and request sanitization.
- Smart caching layer with configurable TTL to reduce redundant LLM calls.
- Metrics and health checks for latency, cache hit rate, token usage, and system status.
- Centralized configuration validation using pydantic-settings.

---

## Project Structure

```text
production-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── agent.py         # LangChain agent and RAG logic
│   ├── cache.py         # Memory/Redis caching mechanism
│   ├── config.py        # Validated configuration settings via Pydantic
│   ├── models.py        # Pydantic schemas for requests and responses
│   ├── monitering.py    # Health and latency metrics instrumentation
│   └── security.py      # Rate limiter and API security utilities
├── tests/               # Unit and integration tests
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies and metadata
├── test.py              # Configuration self-test script
└── README.md            # Project documentation
```

---

## Getting Started

### Prerequisites

- Python 3.12 or later
- Package manager: uv (recommended) or pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mekin-jema/Production-RAG-with-Langchain.git
   cd Production-RAG-with-Langchain
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```
   This command creates a `.venv` and installs dependencies from `pyproject.toml`.

3. Configure environment variables:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PRIMARY_MODEL=gpt-4o-mini
   FALLBACK_MODEL=gpt-4o

   LANGSMITH_TRACING_V2=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_PROJECT=production-api

   APP_ENV=development
   LOG_LEVEL=INFO
   RATE_LIMIT=20/min
   CACHE_TTL_SECONDS=300
   MAX_RETRIES=3
   ```

4. Verify configuration:
   ```bash
   uv run python test.py
   ```

---

## Running the Application

Start the FastAPI server in development mode:

```bash
uv run uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.
The Swagger UI documentation is available at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

### Chat Completion / Agent Execution

- Endpoint: `POST /api/v1/chat`
- Request body:
  ```json
  {
    "message": "Explain the concept of quantum computing briefly.",
    "thread_id": "session_123"
  }
  ```
- Response body:
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

### System Health Status

- Endpoint: `GET /health`
- Response body:
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

### Usage Metrics

- Endpoint: `GET /metrics`
- Response body:
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

## Testing

Run unit and integration tests with pytest:

```bash
uv run pytest
```

---

## License

This project is licensed under the MIT License.
