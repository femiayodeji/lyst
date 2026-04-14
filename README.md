# lyst

A natural-language database assistant. Ask questions in plain English, get SQL queries, tabular results, and auto-generated charts — no SQL knowledge required.

Built with [FastAPI](https://fastapi.tiangolo.com/), [LiteLLM](https://github.com/BerriAI/litellm), and [SQLAlchemy](https://www.sqlalchemy.org/).

## Features

- **Plain English → SQL → Results** — ask a question, the agent writes SQL, runs it, and explains the answer
- **Auto visualization** — chart-friendly results are automatically rendered as bar, line, pie, or doughnut charts
- **Multi-provider LLM** — works with Gemini, Anthropic, OpenAI, Groq, and any LiteLLM-compatible provider
- **Database agnostic** — PostgreSQL, MySQL, SQLite, and any SQLAlchemy-supported engine
- **Schema introspection** — reads table/column/FK metadata so the LLM generates accurate queries
- **Read-only safety** — all generated SQL is validated; only `SELECT` queries are executed
- **Streaming SSE responses** — real-time status updates, SQL, results, charts, and chat streamed to the client
- **Multi-session conversations** — create, switch, and delete named sessions with full history
- **Web UI included** — single-page frontend served at `/` with chat, SQL panel, data table, and charts
- **Runtime DB switching** — change the target database at runtime via the API without restarting

## How It Works

```
User question (plain English)
  → LLM reads the DB schema + system prompt
    → LLM calls execute_sql(generated SELECT query)
      → SQL validated (SELECT only) → executed on DB → columns + rows returned
        → streamed to frontend as a data table
    → LLM calls visualize_data(chart_type, title)
        → streamed to frontend → rendered as a chart
  → LLM generates a plain-English summary of the results
      → streamed to frontend as a chat message
```

The agent loop (`app/agent/loop.py`) drives this cycle for up to 5 iterations, allowing the LLM to retry failed queries or chain multiple tool calls before producing a final answer.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- An API key for your chosen LLM provider

## Quick Start

1. **Clone and install**

   ```bash
   git clone https://github.com/femiayodeji/lyst.git
   cd lyst
   uv sync
   ```

2. **Configure environment**

   Create a `.env` file in the project root:

   ```env
   LYST_LLM_API_KEY=your-api-key
   LYST_DB_CONNECTION=postgresql://user:pass@localhost/mydb
   ```

3. **Start the server**

   ```bash
   uv run uvicorn app.main:app --reload
   ```

   Open `http://localhost:8000` for the web UI, or `http://localhost:8000/docs` for the interactive API docs.

### Docker

```bash
docker compose up --build
```

The container exposes port `8000` and reads configuration from your `.env` file. The `app/static` directory is mounted as a volume for live frontend changes.

## Configuration

All settings are environment variables (set in `.env` or your shell):

| Variable | Description | Default |
|---|---|---|
| `LYST_LLM_API_KEY` | LLM provider API key | *(required)* |
| `LYST_DB_CONNECTION` | SQLAlchemy connection string | *(required)* |
| `LYST_LLM_PROVIDER` | Provider name | `gemini` |
| `LYST_LLM_MODEL` | Model identifier (LiteLLM format) | `gemini/gemini-2.0-flash` |
| `LYST_LLM_BASE_URL` | Custom API base URL | *(provider default)* |
| `LYST_STREAM` | Enable streaming responses | `true` |

### Provider Examples

<details>
<summary><strong>Gemini</strong> (default)</summary>

```env
LYST_LLM_PROVIDER=gemini
LYST_LLM_MODEL=gemini/gemini-2.0-flash
LYST_LLM_API_KEY=your-gemini-api-key
```
</details>

<details>
<summary><strong>Anthropic</strong></summary>

```env
LYST_LLM_PROVIDER=anthropic
LYST_LLM_MODEL=anthropic/claude-3-5-sonnet-20241022
LYST_LLM_BASE_URL=https://api.anthropic.com
LYST_LLM_API_KEY=your-anthropic-api-key
```
</details>

<details>
<summary><strong>OpenAI</strong></summary>

```env
LYST_LLM_PROVIDER=openai
LYST_LLM_MODEL=openai/gpt-4o
LYST_LLM_BASE_URL=https://api.openai.com/v1
LYST_LLM_API_KEY=your-openai-api-key
```
</details>

<details>
<summary><strong>Groq</strong></summary>

```env
LYST_LLM_PROVIDER=groq
LYST_LLM_MODEL=groq/llama-3.3-70b-versatile
LYST_LLM_BASE_URL=https://api.groq.com/openai/v1
LYST_LLM_API_KEY=your-groq-api-key
```
</details>

## API Reference

### Health & Configuration

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check — reports if LLM and DB are configured |
| `GET` | `/config` | View current configuration (API key is masked) |
| `PUT` | `/config/db` | Change the database connection at runtime |

### Schema

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/schema` | Get the current database schema and engine type |
| `POST` | `/schema/load` | Load and cache schema (pass `?force=true` to refresh) |

### Agent

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/agent/stream` | Send a message; returns an SSE stream of agent events |

**Request body:**

```json
{
  "message": "Show total sales by month",
  "history": []
}
```

**SSE event types:**

| Event type | Description |
|---|---|
| `status` | Progress indicator (`Thinking...`, `Executing query...`, `Analyzing results...`) |
| `sql` | The generated SQL query |
| `tool_call` | Tool invocation metadata (tool name + arguments) |
| `result` | Query results (`columns`, `rows`, `row_count`, `success`) |
| `visualize` | Chart recommendation (`chart_type`, `title`) |
| `message_chunk` | Streaming text token from the LLM |
| `message_complete` | Full assembled assistant response |
| `tool_calls` | Summary of all tool calls made |
| `sql_results` | Summary of all SQL results |
| `history` | Updated conversation history (pass back in subsequent requests) |
| `error` | Error message |
| `done` | Stream complete |

### Sessions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/sessions` | List all sessions with the active session ID |
| `POST` | `/sessions` | Create a new session (auto-activated) |
| `GET` | `/sessions/{id}` | Get session details and messages |
| `PUT` | `/sessions/{id}/activate` | Switch to a session |
| `DELETE` | `/sessions/{id}` | Delete a session |

### History

| Method | Endpoint | Description |
|---|---|---|
| `PUT` | `/history` | Save message history to the active session |
| `DELETE` | `/history` | Clear conversation history for the active session |

## Usage Examples

**Ask a question:**

```bash
curl -N -X POST http://localhost:8000/agent/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "How many users signed up this year?"}'
```

**Continue a conversation** (pass back the `history` from the previous response):

```bash
curl -N -X POST http://localhost:8000/agent/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Break that down by month", "history": [...]}'
```

**Switch databases at runtime:**

```bash
curl -X PUT http://localhost:8000/config/db \
  -H "Content-Type: application/json" \
  -d '{"connection": "sqlite:///other.db"}'
```

## Project Structure

```
app/
├── main.py              # FastAPI app, lifespan, middleware, static file serving
├── config.py            # Environment-based configuration (LLM + DB settings)
├── state.py             # In-memory app state: engine cache, schema cache, sessions
├── history.py           # Session CRUD and history management
├── agent/
│   ├── loop.py          # Core agent loop — LLM ↔ tool-call cycle (up to 5 iterations)
│   ├── prompts.py       # System prompt builder (injects schema + guidelines)
│   ├── tools.py         # Tool definitions and handlers (execute_sql, visualize_data, etc.)
│   └── stream.py        # Wraps agent events as Server-Sent Events
├── db/
│   ├── engine.py        # SQLAlchemy engine management, schema introspection, query execution
│   └── schema.py        # Schema caching layer with TTL
├── routes/
│   ├── agent.py         # POST /agent/stream
│   ├── config.py        # GET /health, GET /config, PUT /config/db
│   ├── schema.py        # GET /schema, POST /schema/load
│   └── sessions.py      # Session and history endpoints
└── static/
    └── index.html       # Single-page web UI
tests/
├── test_api.py          # API endpoint tests
└── test_history.py      # Session/history unit tests
```

## Security

- **Read-only queries only** — a regex guard rejects any SQL containing `INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, `ALTER`, `CREATE`, `GRANT`, `REVOKE`, `EXEC`, `EXECUTE`, `MERGE`, or `REPLACE INTO`
- **Schema caching** — schema is cached with a 5-minute TTL to reduce database load
- **No credentials in responses** — the `/config` endpoint masks the API key
- **CORS enabled** — configured with permissive defaults; restrict `allow_origins` in production

## Running Tests

```bash
uv run python -m pytest tests/ -v
```

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.115+
- **LLM Gateway**: [LiteLLM](https://github.com/BerriAI/litellm) 1.82+
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) 2.0+ (PostgreSQL, MySQL, SQLite)
- **Runtime**: Python 3.13, [uv](https://docs.astral.sh/uv/)
- **Containerization**: Docker with multi-stage build

## License

MIT
