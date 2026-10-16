from typing import List, Dict, Any, Optional
import os
import json

def load_json_data(filename: str, default: Any = None) -> Any:
    """Loads and parses an individual JSON data file."""
    path = filename
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else []


def get_research_entities() -> List[Dict[str, Any]]:
    return load_json_data("research_entities.json", [])


def get_research_entity(ticker: str) -> Optional[Dict[str, Any]]:
    t = ticker.upper().strip()
    for e in get_research_entities():
        if e.get("ticker", "").upper() == t:
            return e
    return None