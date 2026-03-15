# lyst

**lyst** is a command-line tool that lets you query your database using plain English, powered by LLMs. It translates natural language questions into SQL, executes them, and summarizes results. Designed for analysts, engineers, and anyone who wants to interact with databases without writing SQL.

## Features

- **Plain English to SQL**: Ask questions in English, get SQL queries and results.
- **LLM-powered**: Supports configurable LLM providers (Anthropic, OpenAI, etc.).
- **Database agnostic**: Works with any SQL database supported by SQLAlchemy.
- **Schema introspection**: Automatically reads your database schema for accurate queries.
- **Configurable**: Easily set LLM and database connection via CLI.
- **History tracking**: Saves session history for review and follow-up questions.
- **Streaming support**: Optionally stream LLM responses.

## Setup

1. **Clone the repository**
	```bash
	git clone <repo-url>
	cd lyst
	```
2. **Install dependencies**
	```bash
	uv sync
	```
3. **Configure LLM and database**
	```bash
	lyst config set --provider <llm-provider> --model <model-name> --base-url <llm-url> --connection <db-connection-string>
	```

## Usage

**Ask a one-off question:**

```bash
lyst ask-question "Show total sales by month"
```

**Start an interactive chat session:**

```bash
lyst chat
```

**Configure your LLM provider and database separately:**

```bash
lyst config llm --provider anthropic --model anthropic/claude-sonnet-4-20250514 --base-url https://api.anthropic.com
lyst config db --connection postgresql://user:pass@localhost/mydb
```

**View current configuration:**

```bash
lyst config show
```

## Example

```
$ lyst ask-question "List top 5 customers by revenue"
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

Use `lyst chat` for follow-up questions — lyst keeps session history for context-aware answers.

## License

MIT
