import json
import os
from typing import Any, Dict, List


BLOCK_ID = "site.links-assets@1.0.0"


def run(inputs: List[str], outputs: List[str]) -> Dict[str, Any]:
    """
    Minimal broken links check. Accepts a JSON file like:
    {"links": [{"href": "/ok", "status": 200}, {"href": "/missing", "status": 404}]}
    """
    print("  Executing site_links_assets block...")

    links = [
        {"href": "/ok", "status": 200},
        {"href": "/missing", "status": 404},
    ]
    for ip in inputs:
        if os.path.isfile(ip) and ip.endswith('.json'):
            with open(ip, 'r') as f:
                cfg = json.load(f)
                links = cfg.get('links', links)
                break

    issues = []
    broken = 0
    for idx, lk in enumerate(links):
        status = int(lk.get('status', 0))
        if status >= 400:
            broken += 1
            href = lk.get('href', '')
            issues.append({
                "id": f"links.broken:{href or idx}",
                "severity": "major",
                "confidence": 0.9,
                "location": {"url": "", "selector": f"a[href='{href}']" if href else ""},
                "evidence": {"type": "http", "note": f"status {status}"},
                "rationale": "Links should not return client or server errors.",
                "suggested_fix": "Update link or fix target resource.",
                "meta": {"status": status}
            })

    status = "pass" if broken == 0 else "fail"
    check_result = {
        "check_id": "links.broken",
        "block_id": BLOCK_ID,
        "status": status,
        "metrics": {"links_total": len(links), "links_broken": broken},
        "issues": issues,
    }

    return {"block_id": BLOCK_ID, "check_results": [check_result]}
