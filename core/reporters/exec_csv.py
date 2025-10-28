import csv
import io
from typing import Any, Dict, List


def _rows(run: Dict[str, Any]) -> List[List[str]]:
    """Extract rows from run record for CSV export."""
    rows: List[List[str]] = [["check_id", "status", "url", "selector", "severity"]]
    results = run.get("results", [])
    for r in results:
        check_id = r.get("check_id", "")
        status = r.get("status", "")
        issues = r.get("issues", []) or []
        if not issues:
            rows.append([check_id, status, "", "", ""])
            continue
        for issue in issues:
            loc = issue.get("location", {}) or {}
            rows.append([
                check_id,
                status,
                loc.get("url", ""),
                loc.get("selector", ""),
                issue.get("severity", ""),
            ])
    return rows


def render(run: Dict[str, Any]) -> str:
    """Render run record as CSV using csv.writer for proper escaping."""
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    for row in _rows(run):
        writer.writerow(row)

    return output.getvalue()
