"""
Minimal plugin contract for blocks that produce structured results.

Blocks may choose to return a dict with the following structure:
{
  "block_id": "brand.palette@1.0.0",
  "check_results": [
    {
      "check_id": "brand.palette-contrast",
      "block_id": "brand.palette@1.0.0",
      "status": "pass|fail|error",
      "metrics": { ... },
      "issues": [
        {
          "id": "<stable-id>",
          "severity": "critical|major|minor|info",
          "confidence": 0.0,
          "location": {"url": "", "selector": "", "viewport": ""},
          "evidence": {"type": "", "note": ""},
          "rationale": "",
          "suggested_fix": "",
          "meta": {}
        }
      ]
    }
  ]
}

Blocks that do not return this dict will still run as part of pipelines; their outputs
are handled via regular files declared in the spec.
"""

from typing import Any, Dict, List, Optional, TypedDict


class Issue(TypedDict, total=False):
    id: str
    severity: str
    confidence: float
    location: Dict[str, str]
    evidence: Dict[str, Any]
    rationale: str
    suggested_fix: str
    meta: Dict[str, Any]


class CheckResult(TypedDict, total=False):
    check_id: str
    block_id: str
    status: str
    metrics: Dict[str, Any]
    issues: List[Issue]


class BlockResult(TypedDict, total=False):
    block_id: str
    check_results: List[CheckResult]

