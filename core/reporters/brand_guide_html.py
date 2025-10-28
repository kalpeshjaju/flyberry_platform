from typing import Any, Dict


TEMPLATE = """<!doctype html>
<html>
  <head>
    <meta charset=\"utf-8\" />
    <title>Brand Guide (Projection)</title>
    <style>
      body {{ font-family: -apple-system, system-ui, Segoe UI, Roboto, sans-serif; margin: 40px; }}
      h1 {{ margin-bottom: 0; }}
      .meta {{ color: #666; }}
      .section {{ margin: 24px 0; }}
      .swatch {{ display: inline-block; width: 80px; height: 40px; margin: 6px; border: 1px solid #ddd; }}
      .token {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: #f5f5f5; padding: 2px 6px; border-radius: 4px; }}
      table {{ border-collapse: collapse; }}
      th, td {{ border: 1px solid #ddd; padding: 6px 10px; }}
    </style>
  </head>
  <body>
    <h1>Brand Guide</h1>
    <div class=\"meta\">Suite: {suite} • Run: {run_id}</div>

    <div class=\"section\">
      <h2>Palettes</h2>
      {palette_html}
    </div>

    <div class=\"section\">
      <h2>Tokens (Color)</h2>
      {token_html}
    </div>

    <div class=\"section\">
      <h2>Issues Summary</h2>
      <table>
        <thead><tr><th>Check</th><th>Severity</th><th>Count</th></tr></thead>
        <tbody>
          {issue_rows}
        </tbody>
      </table>
    </div>
  </body>
</html>
"""


def render(run: Dict[str, Any]) -> str:
    suite = run.get("run", {}).get("suite", "")
    run_id = run.get("run", {}).get("id", "")

    # Palettes from meta if present
    palettes = (run.get("meta", {}) or {}).get("palettes", [])
    palette_html = "".join([
        "".join([f'<div class=\"swatch\" title=\"{c}\" style=\"background:{c}\"></div>' for c in p.get("colors", [])])
        for p in palettes
    ])

    # Color tokens from meta if present
    color_tokens = (run.get("meta", {}) or {}).get("tokens", {}).get("color", {})
    token_html = "<ul>" + "".join([f"<li><span class=token>{k}</span>: {v}</li>" for k, v in color_tokens.items()]) + "</ul>"

    # Issues summary
    counts = {}
    for r in run.get("results", []):
        key = r.get("check_id", "")
        for issue in r.get("issues", []) or []:
            sev = issue.get("severity", "unknown")
            counts.setdefault((key, sev), 0)
            counts[(key, sev)] += 1
    rows = []
    for (check, sev), cnt in sorted(counts.items()):
        rows.append(f"<tr><td>{check}</td><td>{sev}</td><td>{cnt}</td></tr>")

    return TEMPLATE.format(
        suite=suite,
        run_id=run_id,
        palette_html=palette_html or "<em>No palettes found in run meta.</em>",
        token_html=token_html or "<em>No tokens found in run meta.</em>",
        issue_rows="\n" + "\n".join(rows) if rows else "<tr><td colspan=3><em>No issues</em></td></tr>",
    )

