import json
from pathlib import Path
from datetime import datetime

CONFIG_DIR = Path.home() / ".config" / "lyst"
SESSION_FILE = CONFIG_DIR / "session.json"

MAX_HISTORY_EXCHANGES = 10


def _ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_history() -> list[dict]:
    if not SESSION_FILE.exists():
        return []
    try:
        data = json.loads(SESSION_FILE.read_text())
        return data.get("messages", [])
    except (json.JSONDecodeError, KeyError):
        return []


def save_history(messages: list[dict]) -> None:
    _ensure_config_dir()
    SESSION_FILE.write_text(json.dumps({
        "updated_at": datetime.now().isoformat(),
        "messages": messages,
    }, indent=2))


def append_exchange(history: list[dict], user_input: str, assistant_response: str) -> list[dict]:
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": assistant_response})

    max_messages = MAX_HISTORY_EXCHANGES * 2
    if len(history) > max_messages:
        history = history[-max_messages:]

    return history


def clear_history() -> None:
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def history_summary() -> str:
    messages = load_history()
    if not messages:
        return "No active session."
    exchanges = len(messages) // 2
    return f"{exchanges} exchange(s) in current session. ({SESSION_FILE})"