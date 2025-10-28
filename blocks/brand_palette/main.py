import json
import os
from typing import Any, Dict, List, Tuple


BLOCK_ID = "brand.palette@1.0.0"


def _hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    h = hex_color.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join([c*2 for c in h])
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return (r, g, b)


def _rel_luminance(rgb: Tuple[float, float, float]) -> float:
    def _to_lin(c: float) -> float:
        return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055) ** 2.4
    r, g, b = rgb
    r_lin, g_lin, b_lin = _to_lin(r), _to_lin(g), _to_lin(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def _contrast_ratio(c1: str, c2: str) -> float:
    L1 = _rel_luminance(_hex_to_rgb(c1))
    L2 = _rel_luminance(_hex_to_rgb(c2))
    L1, L2 = max(L1, L2), min(L1, L2)
    return (L1 + 0.05) / (L2 + 0.05)


def run(inputs: List[str], outputs: List[str]) -> Dict[str, Any]:
    """
    Validate brand palette color contrast. Inputs may include a JSON file of colors:
    {
      "palette": ["#000000", "#FFFFFF", ...],
      "min_ratio": 4.5
    }
    """
    print("  Executing brand_palette block...")

    # Defaults
    colors: List[str] = ["#111111", "#FFFFFF", "#E63946", "#1D3557", "#F1FAEE"]
    min_ratio: float = 4.5

    for ip in inputs:
        if os.path.isfile(ip) and ip.endswith('.json'):
            with open(ip, 'r') as f:
                cfg = json.load(f)
                colors = cfg.get('palette', colors)
                min_ratio = float(cfg.get('min_ratio', min_ratio))

    total_pairs = 0
    fails = 0
    issues = []
    for i in range(len(colors)):
        for j in range(i+1, len(colors)):
            total_pairs += 1
            c1, c2 = colors[i], colors[j]
            try:
                ratio = _contrast_ratio(c1, c2)
            except Exception:
                continue
            if ratio < min_ratio:
                fails += 1
                issues.append({
                    "id": f"brand.palette-contrast:{c1}:{c2}",
                    "severity": "major",
                    "confidence": 0.95,
                    "location": {},
                    "evidence": {"type": "color_pair", "note": f"{c1} vs {c2}"},
                    "rationale": f"Contrast ratio {ratio:.2f} below minimum {min_ratio}",
                    "suggested_fix": "Increase contrast or adjust palette steps",
                    "meta": {"ratio": round(ratio, 2)}
                })

    status = "pass" if fails == 0 else "fail"
    check_result = {
        "check_id": "brand.palette-contrast",
        "block_id": BLOCK_ID,
        "status": status,
        "metrics": {
            "pairs_tested": total_pairs,
            "pairs_failing": fails,
            "min_ratio": min_ratio
        },
        "issues": issues
    }

    # Optionally write any declared outputs
    for op in outputs or []:
        if op.endswith('.json'):
            with open(op, 'w') as f:
                json.dump({"palette": colors}, f, indent=2)

    # Include palette in run meta by returning it as part of block result meta-hint
    return {
        "block_id": BLOCK_ID,
        "check_results": [check_result],
        "meta": {"palettes": [{"name": "default", "colors": colors}]}
    }
