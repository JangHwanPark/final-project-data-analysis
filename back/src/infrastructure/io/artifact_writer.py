import json
from pathlib import Path
from core.config import ENCODING

def write_json(data: dict, path: Path) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open("w", encoding=ENCODING) as f:
    json.dump(data, f, ensure_ascii=False, indent=2)