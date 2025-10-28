import json
import os
from typing import Any, Dict, List


BLOCK_ID = "brand.tokens@1.0.0"


def run(inputs: List[str], outputs: List[str]) -> Dict[str, Any]:
    """
    Validate token naming and generate a minimal color token set if requested.
    Input JSON example:
    {
      "tokens": {"color": {"fb-primary": "#1D3557", "primary": "#E63946"}},
      "naming_prefix": "fb-"
    }
    """
    print("  Executing brand_tokens block...")

    tokens: Dict[str, Any] = {"color": {"fb-primary": "#1D3557", "fb-accent": "#E63946"}}
    prefix = "fb-"

    for ip in inputs:
        if os.path.isfile(ip) and ip.endswith('.json'):
            with open(ip, 'r') as f:
                cfg = json.load(f)
                tokens = cfg.get('tokens', tokens)
                prefix = cfg.get('naming_prefix', prefix)

    issues = []
    total = 0
    bad = 0
    for group, mp in tokens.items():
        if not isinstance(mp, dict):
            continue
        for name, _ in mp.items():
            total += 1
            if not name.startswith(prefix):
                bad += 1
                issues.append({
                    "id": f"brand.tokens-naming:{name}",
                    "severity": "minor",
                    "confidence": 0.9,
                    "location": {},
                    "evidence": {"type": "token_name", "note": name},
                    "rationale": f"Token names must start with prefix '{prefix}'",
                    "suggested_fix": f"Rename to '{prefix}{name}'",
                    "meta": {"group": group}
                })

    status = "pass" if bad == 0 else "fail"
    check_result = {
        "check_id": "brand.tokens-naming",
        "block_id": BLOCK_ID,
        "status": status,
        "metrics": {"tokens_total": total, "tokens_bad": bad, "prefix": prefix},
        "issues": issues
    }

    # Optionally write outputs
    for op in outputs or []:
        if op.endswith('.json'):
            with open(op, 'w') as f:
                json.dump({"tokens": tokens}, f, indent=2)

    return {
        "block_id": BLOCK_ID,
        "check_results": [check_result],
        "meta": {"tokens": tokens}
    }
