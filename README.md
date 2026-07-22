
# Production LLM and RAG API

This repository contains a production-oriented API for operating LLM agents with Retrieval-Augmented Generation (RAG). The service is implemented using FastAPI and LangChain and emphasizes configuration-driven behavior, observability, caching, and secure operation.
---

## Key features

- Asynchronous API built on `FastAPI` for low-latency request handling.
- Agent orchestration and document retrieval via `LangChain`.
- Observability integration (LangSmith-compatible tracing and logging).
- Configuration-driven security: API keys, rate limiting, and request sanitization.
- Cache abstraction supporting in-memory and Redis with configurable TTL and metrics.
- Health checks, metrics, and tests to validate correctness and availability.
---

## Getting started (development)

Prerequisites

- Python 3.12 or later
- Git

Clone the repository and change into the project directory:

```bash
git clone https://github.com/Mekin-jema/Production-RAG-with-Langchain.git
cd Production-RAG-with-Langchain
```

Create a virtual environment and install dependencies. Use your preferred tooling; examples shown for `venv`/`pip` and `uv`.

```bash
# Using python venv + pip
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Or, if you use the 'uv' helper: (project-specific)
uv sync
```

Environment configuration

Copy and populate environment variables. The service reads configuration from a `.env` file and environment variables.

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY, LANGSMITH_API_KEY, and other values
```

Run the app locally in development mode:

```bash
uv run uvicorn app.main:app --reload
```

The OpenAPI docs are available at `http://127.0.0.1:8000/docs`.
---

## API usage

The API exposes endpoints for chat/agent execution, health checks, and metrics. Authentication is typically by API key passed in the `Authorization` header as a Bearer token.

POST /api/v1/chat

Request

```json
{
  "message": "Summarize the README in one sentence",
  "thread_id": "demo-1",
  "options": {
    "max_tokens": 256
  }
}
```

Example curl

```bash
curl -s -X POST "http://127.0.0.1:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <API_KEY>" \
  -d '{"message":"Summarize the README in one sentence","thread_id":"demo-1"}'
```

Typical response

```json
{
  "response": "A production-ready FastAPI and LangChain scaffold for RAG-powered LLM agents.",
  "thread_id": "demo-1",
  "model_used": "gpt-4o-mini",
  "cached": false,
  "processing_time_ms": 250.0
}
```

GET /health

Returns application and dependency health status (database/cache/OpenAI connectivity).

GET /metrics

Exposes runtime metrics such as request counts, latencies, cache hit rate, and token usage. Hook this endpoint into your monitoring stack.
---

## Project structure

```
production-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entrypoint
│   ├── agent.py         # LangChain agent + RAG orchestration
│   ├── cache.py         # Cache abstraction (memory/Redis)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── models.py        # Request/response schemas
│   ├── monitoring.py    # Metrics & health checks
│   └── security.py      # API-key validation & rate limiting
├── tests/               # Unit & integration tests
├── pyproject.toml       # Project metadata + dependencies
├── test.py              # Quick self-check script
└── README.md            # Project documentation
```
---

## Observability and metrics

- `/health` — application readiness and dependency checks
- `/metrics` — runtime metrics for scraping (compatible with Prometheus-style collectors)
- Optionally integrate LangSmith for structured traces and run evaluations
---

## Testing

Run unit and integration tests using `pytest`:

```bash
uv run pytest
```

Or run the quick configuration check script:

```bash
python test.py
```
---

## Deployment and production considerations

- Use Redis or another external cache for multi-instance deployments (`CACHE_URL`).
- Run the application behind a reverse proxy (for example, NGINX) and terminate TLS at the proxy.
- Configure process managers (systemd, supervisord) or container orchestrators for high availability.
- Tune `RATE_LIMIT` and `CACHE_TTL_SECONDS` to balance cost and responsiveness.
- Monitor token and API usage and set alerts for anomalous consumption.

---


## Contributing

Contributions are welcome. For significant changes, please open an issue to discuss the approach before submitting a pull request. Maintain the repository style and run tests locally.

## License

This project is provided under the MIT License. See the `LICENSE` file for details if it is present.

## Contact

For questions about this repository, open an issue or contact the maintainer via the project hosting platform.
