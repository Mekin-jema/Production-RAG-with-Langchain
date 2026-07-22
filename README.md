# Production LLM and RAG API

This repository contains a production-oriented API for operating LLM agents with Retrieval-Augmented Generation (RAG). The service is implemented using `FastAPI`, `LangChain`, and optionally `LangGraph` for stateful agent workflows. The codebase includes production-grade concerns (security, caching, metrics) and a set of advanced reference patterns for real-world RAG deployments.

---

## Key features

- Asynchronous API built on `FastAPI` for low-latency request handling.
- Agent orchestration and document retrieval via `LangChain`.
- Observability integration (LangSmith-compatible tracing and logging).
- Configuration-driven security: API keys, rate limiting, and request sanitization.
- Cache abstraction supporting in-memory and Redis with configurable TTL and metrics.
- Health checks, metrics, and tests to validate correctness and availability.

The repository also contains advanced patterns and reference implementations demonstrating:

- LangGraph-based agent workflows (stateful, cyclic graphs) for production-grade agent orchestration.
- Agentic RAG: retrieve → evaluate → rewrite/retry → generate, enabling self-correcting retrieval loops.
- GraphRAG concepts and examples: building knowledge graphs from documents for multi-hop reasoning and relationship traversal.
- Contextual retrieval, late-chunking, and multimodal RAG patterns useful for production deployments.

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

Create a virtual environment and install dependencies. Use your preferred tooling; examples shown for `venv`/`pip` and the project helper `uv`.

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

Note: The project uses optional advanced modules under the `advanced/` folder illustrating Agentic RAG, GraphRAG, contextual retrieval, late-chunking, and multimodal patterns. These are educational references and demo scripts you can adapt for production use.

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

Additional endpoints and behaviors

- `POST /chat` — Main chat endpoint wired to the LangGraph-based agent. Request/response models are defined in `app/models.py`.
- `GET /cache/stats` — Returns cache internals and hit/miss counts for the configured cache implementation.

Authentication

The service expects an API key passed in the `Authorization: Bearer <KEY>` header. The validation logic is implemented in `app/security.py` and can be adapted to your auth system.

---

## Project structure

```
production-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entrypoint
│   ├── agent.py         # LangChain/LangGraph agent orchestration
│   ├── cache.py         # Cache abstraction (memory/Redis)
│   ├── config.py        # Settings (pydantic-settings)
│   ├── models.py        # Request/response schemas
│   ├── monitoring.py    # Metrics & health checks
│   └── security.py      # API-key validation & rate limiting
├── advanced/            # Reference scripts for advanced RAG patterns
├── tests/               # Unit & integration tests
├── pyproject.toml       # Project metadata + dependencies
├── test.py              # Quick self-check script
└── README.md            # Project documentation
```

Key modules

- `app/main.py` — FastAPI application wiring, lifespan management, endpoint handlers, and configuration glue.
- `app/agent.py` — Production `ProductionAgent` implemented using LangGraph state machines. Handles retry/fallback, LangSmith tracing, and model orchestration.
- `app/cache.py` — Cache abstraction layer used by the API to reduce redundant LLM calls.
- `app/config.py` — Centralized configuration using pydantic settings.
- `app/security.py` — Input/output sanitization, PII masking, and API key validation.
- `app/monitoring.py` — Metrics collection, structured logging helpers, and request timing utilities.
- `advanced/` — Educational examples and reference implementations for Agentic RAG, GraphRAG, contextual retrieval, late-chunking, and multimodal RAG.

---

## Observability and metrics

- `/health` — application readiness and dependency checks
- `/metrics` — runtime metrics for scraping (compatible with Prometheus-style collectors)
- Optionally integrate LangSmith for structured traces and run evaluations

Integration tips

- Configure LangSmith tracing via environment variables in `app/config.py` so traces include agent step names and graph transitions.
- Expose `/metrics` and scrape with Prometheus; record cache hit rate and agent decision counts (rewrite vs generate vs fallback).

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

Development notes

- Tests in `tests/` are fast and deterministic; add unit tests for new agent nodes and grading logic.
- When running demos in `advanced/`, set `OPENAI_API_KEY` and any other API keys in a local `.env` file to avoid leaking secrets.

---

## Patterns and recommendations (detailed)

This section summarizes the advanced lessons included in `advanced/` and how to apply them in production.

1) Long Context vs RAG (`advanced/01_long_context_vs_rag.py`)

- Cost model: stuffing large contexts into the model increases token costs and latency. The lesson script includes a cost comparison example (100k tokens vs retrieving a handful of chunks) and shows how RAG can be orders-of-magnitude cheaper per query at scale.
- Latency: large contexts increase model processing time; RAG adds retrieval time but generally has lower end-to-end latency for large corpora.
- Decision framework: use long-context when a single, up-to-date context is small enough and latency/cost are acceptable; use RAG for large, frequently changing corpora or when you need cheaper recurring queries.

2) Contextual Retrieval (`advanced/02_contextual_retrieval.py`)

- Problem: chunking removes document-level context and can make chunks ambiguous.
- Solution: generate a short contextual prefix for each chunk (document title, key entities, brief summary) using an LLM, then prepend that prefix to the chunk before embedding. The script provides `create_contextual_chunks()` showing a production-ready approach.

3) Late Chunking (`advanced/03_late_chunking.py`)

- Problem: early chunking embeds chunks independently and loses cross-chunk context (pronouns, references).
- Solution: embed the full document (or use token-level embeddings) then slice pooled embeddings into chunk vectors. This preserves the document context and improves retrieval accuracy.

4) Agentic RAG (`advanced/04_agentic_rag.py`)

- Pattern: `retrieve -> grade -> [rewrite -> retrieve]* -> generate -> fallback`.
- Grade step: an LLM assigns relevance scores to retrieved docs; the router decides whether to rewrite the query or proceed to generation.
- Rewrite step: an LLM rewrites the query to improve retrieval; the workflow loops until relevance thresholds or retry limits are reached.
- Implementation notes: the script demonstrates a `StateGraph` with nodes (`retrieve`, `grade`, `rewrite`, `generate`, `fallback`) and a routing function `should_retry_or_generate()` that encapsulates the policy.

5) GraphRAG (`advanced/05_graphrag_intro.py`)

- Concept: extract entities and relations from documents into a knowledge graph; execute traversal for multi-hop queries (e.g., "Who works in the same department as X's assistant?").
- Use cases: relationship queries, organizational structure lookups, multi-hop reasoning that vector search can't easily handle.
- Implementation options: Microsoft's GraphRAG library, LangGraph + Neo4j, or LlamaIndex Knowledge Graph Index. The lesson shows a conceptual pipeline: extract entities → build graph → perform traversal and community summarization.

6) Multimodal RAG (`advanced/06_multimodal_rag.py`)

- Problem: text extraction from visual documents (PDFs) often loses table structure, charts, and layout.
- Solution: convert pages to images, embed images or use a vision-capable LLM (e.g., GPT-4V) for retrieval and answering. The lesson demonstrates converting PDF pages to images and using a vision LLM to interpret retrieved pages.

Code pointers

- `app/agent.py` — production LangGraph agent showing retry/fallback and model orchestration.
- `advanced/04_agentic_rag.py` — reference implementation of agentic RAG (grading, rewrite, loop).
- `advanced/05_graphrag_intro.py` — example knowledge graph build and traversal functions.
- `advanced/02_contextual_retrieval.py` and `advanced/03_late_chunking.py` — chunking and embedding strategies.

Recommended environment variables (example keys used across demos)

```env
OPENAI_API_KEY=...
PRIMARY_MODEL=gpt-4o-mini
FALLBACK_MODEL=gpt-4o
LANGSMITH_API_KEY=...
CACHE_TTL_SECONDS=300
RATE_LIMIT=20/min
```

Best practices

- Evaluate retrieval quality using a grading step in development before enabling production generation.
- Start with in-memory cache for local testing, then migrate to Redis for multi-instance deployments.
- Add deterministic unit tests for `security` and `cache` layers; mock LLM calls in CI for integration workflows.
- Instrument metrics for `rewrite` vs `generate` decisions, cache hit rates, average relevance scores, and model costs.

FAQ

- Q: When should I use GraphRAG vs vector RAG?
  A: Use GraphRAG when queries require relationship traversal or multi-hop reasoning. Use vector RAG for semantic or topical retrieval. They can be combined: graph traversal to find related entities, then vector retrieval for document content.

- Q: Is Agentic RAG necessary for all use cases?
  A: No. Agentic RAG is recommended when retrieval quality matters and iteration is affordable. It increases accuracy for complex queries but adds complexity and more LLM calls.

---

## Contributing

Contributions are welcome. For significant changes, please open an issue to discuss the approach before submitting a pull request. Run tests locally and follow repository style.

## License

This project is provided under the MIT License. See the `LICENSE` file for details if it is present.

## Contact

For questions about this repository, open an issue or contact the maintainer via the project hosting platform.
