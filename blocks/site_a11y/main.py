import os
import re
from typing import Any, Dict, List


BLOCK_ID = "site.a11y@1.0.0"
IMG_RE = re.compile(r"<img\b([^>]+)>", re.IGNORECASE)
ALT_RE = re.compile(r"alt\s*=\s*\"([^\"]*)\"|alt\s*=\s*'([^']*)'", re.IGNORECASE)
HIDDEN_RE = re.compile(r"aria-hidden\s*=\s*\"true\"|role\s*=\s*\"presentation\"", re.IGNORECASE)


def run(inputs: List[str], outputs: List[str]) -> Dict[str, Any]:
    """
    Minimal a11y check: flag <img> missing alt or alt="" unless decorative.
    Accepts an HTML file path in inputs; if none found, uses a baked sample.
    """
    print("  Executing site_a11y block...")

    html = None
    for ip in inputs:
        if os.path.isfile(ip) and ip.endswith('.html'):
            with open(ip, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
                break
    if html is None:
        html = "<main><img src=\"/hero.png\"><a href=\"/ok\">Ok</a></main>"

    issues = []
    total_imgs = 0
    missing_alt = 0
    for m in IMG_RE.finditer(html):
        total_imgs += 1
        attrs = m.group(1)
        if HIDDEN_RE.search(attrs or ""):
            continue
        alt_match = ALT_RE.search(attrs or "")
        alt_val = (alt_match.group(1) if alt_match else "") or (alt_match.group(2) if alt_match else "")
        if alt_val is None or alt_val.strip() == "":
            missing_alt += 1
            issues.append({
                "id": f"a11y.img-alt:{total_imgs}",
                "severity": "major",
                "confidence": 0.9,
                "location": {"selector": f"img:nth-of-type({total_imgs})"},
                "evidence": {"type": "dom", "note": "img missing alt"},
                "rationale": "Images must have meaningful alternative text.",
                "suggested_fix": "Add descriptive alt text or mark decorative.",
                "meta": {"wcag": "1.1.1"}
            })

    status = "pass" if missing_alt == 0 else "fail"
    check_result = {
        "check_id": "a11y.img-alt",
        "block_id": BLOCK_ID,
        "status": status,
        "metrics": {"total_images": total_imgs, "missing_alt": missing_alt},
        "issues": issues,
    }

    return {"block_id": BLOCK_ID, "check_results": [check_result]}

