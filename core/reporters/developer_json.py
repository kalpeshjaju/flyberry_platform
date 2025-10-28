import json
from typing import Any, Dict


def render(run: Dict[str, Any]) -> str:
    """
    Pretty JSON projection identical to canonical with stable formatting.
    Returns string content.
    """
    return json.dumps(run, indent=2, ensure_ascii=False)

