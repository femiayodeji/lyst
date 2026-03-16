# lyst

A command-line tool that lets you query your database using plain English. Ask a question, get SQL + results + a summary — no SQL writing required.

Powered by LLMs (via [LiteLLM](https://github.com/BerriAI/litellm)) and [SQLAlchemy](https://www.sqlalchemy.org/), lyst connects to your database, reads its schema, and generates accurate queries from natural language.

## Features

- **Plain English to SQL** — ask questions in natural language, get SQL queries and results
- **Multi-provider LLM support** — works with Anthropic, OpenAI, and any LiteLLM-compatible provider
- **Database agnostic** — connects to PostgreSQL, MySQL, SQLite, and any SQLAlchemy-supported database
- **Auto schema introspection** — reads your database schema for accurate query generation
- **Interactive chat mode** — ask follow-up questions with full conversation context
- **Session history** — maintains context across queries for smarter responses

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- An API key for your LLM provider (e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`)

## Setup

1. **Clone and install**
	```bash
	git clone <repo-url>
	cd lyst
	uv sync
	```

2. **Set your LLM API key**
	```bash
	export LYST_LLM_API_KEY=sk-...
	```

3. **Configure LLM and database**

	Set everything at once:
	```bash
	lyst config set \
	  --provider anthropic \
	  --model anthropic/claude-sonnet-4-20250514 \
	  --base-url https://api.anthropic.com \
	  --connection postgresql://user:pass@localhost/mydb
	```

	Or configure them separately:
	```bash
	lyst config llm --provider anthropic --model anthropic/claude-sonnet-4-20250514 --base-url https://api.anthropic.com
	lyst config db --connection postgresql://user:pass@localhost/mydb
	```

4. **Verify your configuration**
	```bash
	lyst config show
	```

	Configuration is stored at `~/.config/lyst/config.json`.

## Usage

**Ask a question directly:**

```bash
lyst "Show total sales by month"
```

## Example

```
$ lyst "List top 5 customers by revenue"

Generated SQL:
SELECT customer, SUM(revenue) FROM sales GROUP BY customer ORDER BY SUM(revenue) DESC LIMIT 5;

┏━━━━━━━━━━━━┳━━━━━━━━━┓
┃ customer   ┃ revenue ┃
┡━━━━━━━━━━━━╇━━━━━━━━━┩
│ Acme Corp  │ 50000   │
│ Globex     │ 42000   │
│ ...        │ ...     │
└────────────┴─────────┘

Summary: The top 5 customers by revenue are Acme Corp, Globex, ...
```

## License

MIT
