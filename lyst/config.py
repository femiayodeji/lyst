from dataclasses import dataclass
import os    
import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "lyst"
CONFIG_FILE = CONFIG_DIR / "config.json"

@dataclass
class LLMConfig:
    provider: str
    model: str
    base_url: str
    stream: bool

@dataclass
class DBConfig:
    connection: str

@dataclass
class Config:
    llm: LLMConfig
    db: DBConfig

def _ensure_config_dir():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

def load_config() -> Config:
    _ensure_config_dir()
    if not CONFIG_FILE.exists():
        return Config(llm=LLMConfig(provider="", model="", base_url="", stream=False), db=DBConfig(connection=""))
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    
    llm_data = data.get("llm", {})
    db_data = data.get("db", {})
    llm_config = LLMConfig(**llm_data) if llm_data else LLMConfig(provider="", model="", base_url="", stream=False)
    db_config = DBConfig(**db_data) if db_data else DBConfig(connection="")
    
    return Config(llm=llm_config, db=db_config)

def save_config(config: Config):
    _ensure_config_dir()
    llm = config.llm or LLMConfig(provider="", model="", base_url="", stream=False)
    db = config.db or DBConfig(connection="")
    data = {
        "llm": {
            "provider": llm.provider,
            "model": llm.model,
            "base_url": llm.base_url,
            "stream": llm.stream
        },
        "db": {
            "connection": db.connection
        }
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def show_config():
    try:
        config = load_config()
        api_key_Status = "Set" if os.environ.get("LYST_LLM_API_KEY") else "Not Set"
        print(json.dumps({
            "llm": {
                "provider": config.llm.provider,
                "model": config.llm.model,
                "api_key": api_key_Status,
                "base_url": config.llm.base_url,
                "stream": config.llm.stream
            },
            "db": {
                "connection": config.db.connection
            }
        }, indent=4))
    except FileNotFoundError:
        print("No configuration found. Please run 'lyst config set' to create one.")

def set_config(provider: str, model: str, base_url: str, stream: bool, connection: str):
    config = Config(
        llm=LLMConfig(provider=provider, model=model, base_url=base_url, stream=stream),
        db=DBConfig(connection=connection)
    )
    save_config(config)
