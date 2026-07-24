# Production LLM and RAG API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI: 0.110+](https://img.shields.io/badge/FastAPI-0.110%2B-green.svg)](https://fastapi.tiangolo.com/)

A production-grade, asynchronous API scaffold for operating stateful LLM agents with Retrieval-Augmented Generation (RAG). Built using **FastAPI**, **LangChain**, and **LangGraph**, this repository demonstrates enterprise-ready concerns (security, caching, metrics) alongside advanced reference patterns for real-world RAG deployments.

---

## 🌟 Key Features

*   ⚡ **High Performance:** Built on **FastAPI** utilizing Python's `asyncio` for low-latency request handling.
*   🧠 **Stateful Agent Workflows:** Complex agent orchestration via **LangGraph** (supporting cyclic graph transitions and execution history).
*   🛡️ **Production-Grade Security:**
    *   API Key authentication and authorization.
    *   Rate limiting policies.
    *   Input/Output sanitization and PII masking.
*   💾 **Advanced Caching Layer:** In-memory and Redis-backed caching strategies with configurable Time-To-Live (TTL) and monitoring metrics to save LLM costs.
*   📊 **Observability & Monitoring:**
    *   Out-of-the-box support for LangSmith tracing.
    *   Prometheus-compatible `/metrics` endpoint.
    *   System health check `/health` endpoints.
*   🎓 **Advanced RAG Patterns:** Reference implementations for Contextual Retrieval, Late Chunking, Agentic Self-Correcting RAG, GraphRAG, and Multimodal processing.

---

## 🛠️ Getting Started

### Prerequisites

*   Python 3.12 or later
*   Git
*   Redis (optional, for persistent caching)

### 1. Clone the Repository

```bash
git clone https://github.com/Mekin-jema/Production-RAG-with-Langchain.git
cd Production-RAG-with-Langchain
```

### 2. Set Up Virtual Environment

You can install dependencies using the standard Python environment tools or the project-specific `uv` package manager:

```bash
# Option A: Using python venv & pip
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Option B: Using the uv helper (Recommended)
uv sync
```

### 3. Environment Configuration

Copy the example environment file and populate your API credentials:

```bash
cp .env.example .env
```

Ensure the following variables are set in your `.env`:

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | OpenAI API key for completions & embeddings | `sk-proj-...` |
| `PRIMARY_MODEL` | Default model used for chat/generation | `gpt-4o-mini` |
| `FALLBACK_MODEL` | Secondary model used for agent retry loops | `gpt-4o` |
| `LANGSMITH_API_KEY` | API key for LangSmith tracing & evaluation | `lsv2_pt_...` |
| `CACHE_TTL_SECONDS` | TTL for cache entries | `300` |
| `RATE_LIMIT` | API request rate limit | `20/min` |

### 4. Run the API Locally

Start the local development server:

```bash
uv run uvicorn app.main:app --reload
```

Once running, access the interactive OpenAPI documentation at **http://127.0.0.1:8000/docs**.

---

## 🔌 API Usage

The API exposes endpoints for chat, agent execution, caching statistics, health checks, and metrics. Authentication is handled via a Bearer token in the `Authorization` header.

### Main Chat Endpoint (`POST /api/v1/chat`)

Processes a query through the LangGraph-based agent.

#### Request Example

```bash
curl -s -X POST "http://127.0.0.1:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "message": "Summarize the project structure in one sentence",
    "thread_id": "session-123",
    "options": {
      "max_tokens": 256
    }
  }'
```

#### Response Example

```json
{
  "response": "A production-ready FastAPI and LangChain scaffold for RAG-powered LLM agents.",
  "thread_id": "session-123",
  "model_used": "gpt-4o-mini",
  "cached": false,
  "processing_time_ms": 250.0
}
```

### Additional Endpoints

*   `GET /health` — Check the application readiness and dependency status.
*   `GET /metrics` — Prometheus-compatible system metrics.
*   `GET /cache/stats` — Detailed cache statistics (hits, misses, total keys).

---

## 📂 Project Structure

```text
production-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entrypoint and route setups
│   ├── agent.py         # LangChain & LangGraph state machine definitions
│   ├── cache.py         # Cache abstractions (Redis & In-Memory backends)
│   ├── config.py        # Application settings and configuration (Pydantic)
│   ├── models.py        # Request & Response schemas (Pydantic models)
│   ├── monitoring.py    # System metrics, logging helpers, & timing decorators
│   └── security.py      # Rate limiting, API-key verification, & input sanitization
├── advanced/            # Reference scripts & notebooks for advanced RAG patterns
│   ├── 01_long_context_vs_rag.py
│   ├── 02_contextual_retrieval.py
│   ├── 03_late_chunking.py
│   ├── 04_agentic_rag.py
│   ├── 05_graphrag_intro.py
│   └── 06_multimodal_rag.py
├── tests/               # Unit and integration test suites
├── pyproject.toml       # Project metadata, dependencies, and tool settings
├── test.py              # Quick workspace self-check script
└── README.md            # Repository documentation
```

---

## 🚀 Advanced RAG Reference Patterns

The `advanced/` directory contains educational reference implementations designed for adaptation into production environments:

### 1. Long Context vs. RAG (`advanced/01_long_context_vs_rag.py`)
Compares performance, latency, and cost implications between stuffing an entire document corpus into an LLM's context window versus retrieving specific chunks using RAG.

### 2. Contextual Retrieval (`advanced/02_contextual_retrieval.py`)
Precludes chunk ambiguity by utilizing an LLM to generate a short contextual prefix (document metadata, key themes) and prepending it to each chunk before indexing.

### 3. Late Chunking (`advanced/03_late_chunking.py`)
Computes embeddings on full text segments first, and then divides token-level embeddings into chunk vectors. This preserves cross-chunk semantic references (e.g., pronouns).

### 4. Agentic RAG (`advanced/04_agentic_rag.py`)
An iterative flow: `Retrieve -> Grade -> [Rewrite -> Retrieve]* -> Generate/Fallback`. The system grades retrieved documents and loops to rewrite the query if relevance metrics fall below thresholds.

### 5. GraphRAG (`advanced/05_graphrag_intro.py`)
Introduces knowledge graph construction (extracting entities and relations) and traversal for multi-hop questions where vector distance search alone is insufficient.

### 6. Multimodal RAG (`advanced/06_multimodal_rag.py`)
A demonstration of parsing and querying documents containing visual and structural layouts (e.g. PDFs with charts, images, and tables) by converting pages to images and retrieving them using vision-capable LLMs.

---

## 🧪 Testing

The repository uses `pytest` for unit and integration tests.

### Run all tests
```bash
uv run pytest
```

### Run quick self-check script
```bash
python test.py
```

*Note: For the advanced pattern scripts in `advanced/`, ensure your local `.env` has appropriate keys to avoid runtime errors during testing.*

---

## 🤝 Contributing

Contributions are welcome! If you would like to submit new features, improvements, or bug fixes:
1. Open an issue to discuss your proposed change.
2. Fork the repository.
3. Commit changes to your branch and run tests locally.
4. Submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 📞 Contact

For any questions, feedback, or support requests, please open an issue in the project's repository.
