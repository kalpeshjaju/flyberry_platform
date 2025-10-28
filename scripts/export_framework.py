#!/usr/bin/env python3
"""
Export framework files and a human-readable manifest from mapping.

- Reads: framework_mapping.yaml
- Parses source HTML in docs/ to enrich items with content_excerpt when anchor found
- Writes: framework_export/<act>/<section>/<filename>
- Writes: FRAMEWORK_STRUCTURE_COMPLETE.md (exact style)
"""

import json
import re
from pathlib import Path
from datetime import datetime

import yaml
from bs4 import BeautifulSoup
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXPORT = ROOT / "framework_export"
MAPPING = ROOT / "framework_mapping.yaml"
MANIFEST = ROOT / "FRAMEWORK_STRUCTURE_COMPLETE.md"
MANIFEST_EXPORT = EXPORT / "FRAMEWORK_STRUCTURE_COMPLETE.md"


def load_mapping():
    return yaml.safe_load(MAPPING.read_text(encoding="utf-8"))


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def read_html(path_rel: str) -> Optional[BeautifulSoup]:
    # path_rel like "docs/act-1-who-we-are.html#anchor"
    if not path_rel.startswith("docs/"):
        return None
    html_path = ROOT / path_rel.split("#")[0]
    if not html_path.exists():
        return None
    return BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")


from typing import Tuple
import re as _re

def extract_excerpt(source_hint: str) -> Tuple[Optional[str], dict, bool]:
    # Returns (excerpt, lineage)
    if not source_hint.startswith("docs/"):
        return None, {"type": "none"}, False

    parts = source_hint.split("#", 1)
    doc_path = parts[0]
    anchor = parts[1] if len(parts) > 1 else None
    soup = read_html(source_hint)
    if soup is None:
        return None, {"type": "html", "path": doc_path, "anchor": anchor, "confidence": "low"}, False

    node = None
    if anchor:
        node = soup.find(id=anchor)
    if node is None:
        # try matching normalized id
        norm = re.sub(r"[^a-z0-9\-]", "-", (anchor or "").lower())
        node = soup.find(id=norm)

    if node is None:
        return None, {"type": "html", "path": doc_path, "anchor": anchor, "confidence": "low"}, False

    # Collect text until next h2/h3 or up to ~400 chars
    texts = []
    cur = node
    limit = 200
    while cur is not None:
        cur = cur.find_next()
        if cur is None:
            break
        if cur.name in ("h2", "h3"):
            break
        if cur.name in ("p", "li") and cur.get_text(strip=True):
            texts.append(cur.get_text(strip=True))
        if sum(len(t) for t in texts) > limit:
            break

    combined = " ".join(texts)
    # normalize whitespace and trim
    combined = _re.sub(r"\s+", " ", combined).strip()
    excerpt = (combined[:limit]) if combined else None
    return (excerpt or None), {"type": "html", "path": doc_path, "anchor": anchor, "confidence": "medium"}, True


def write_item_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export_from_mapping(mapping: dict) -> dict:
    ensure_dir(EXPORT)
    summary = {}
    manifest_items = []

    for act in mapping.get("acts", []):
        act_slug = act["slug"]
        act_dir = EXPORT / act_slug
        ensure_dir(act_dir)
        act_count = 0
        # prepare per-act STRUCTURE.md lines
        act_lines = [f"# {act['number']}: {act['name']}", ""]

        for section in act.get("sections", []):
            sec_dir = act_dir / section["slug"]
            ensure_dir(sec_dir)

            items = section.get("items", [])
            act_lines.append(f"## {section['code']} {section['name']} ({len(items)} files)")
            act_lines.append("")
            for idx, item in enumerate(items, start=1):
                act_count += 1
                file_path = sec_dir / item["filename"]
                source_hint = item.get("source_hint", "")
                excerpt, lineage, has_anchor = extract_excerpt(source_hint)
                item_id = f"{section['code']}.{idx}"

                payload = {
                    "id": item_id,
                    "title": item.get("title", item["filename"]),
                    "section": f"{section['code']} {section['name']}",
                    "source_hint": source_hint,
                    "status": "draft" if excerpt else "todo",
                    "lineage": lineage,
                    "content_excerpt": excerpt,
                    "has_anchor": has_anchor,
                    "updatedAt": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                }

                write_item_json(file_path, payload)
                # per-act structure line
                act_lines.append(f"- {item_id} {item['filename']}")

                # global machine manifest item
                manifest_items.append({
                    "id": item_id,
                    "act_number": act["number"],
                    "act_name": act["name"],
                    "act_slug": act_slug,
                    "section_code": section["code"],
                    "section_name": section["name"],
                    "section_slug": section["slug"],
                    "filename": item["filename"],
                    "path": str(file_path.relative_to(ROOT)),
                    "title": payload["title"],
                    "source_hint": source_hint,
                    "status": payload["status"],
                    "lineage": lineage,
                    "updatedAt": payload["updatedAt"],
                })
            act_lines.append("")

        # write per-act STRUCTURE.md
        (act_dir / "STRUCTURE.md").write_text("\n".join(act_lines) + "\n", encoding="utf-8")

        summary[act_slug] = act_count

    # write machine-readable global manifest
    (EXPORT / "manifest.json").write_text(
        json.dumps({"generatedAt": datetime.utcnow().isoformat(timespec="seconds") + "Z", "items": manifest_items}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return summary


def write_manifest(mapping: dict, counts: dict):
    lines = ["---", "  Complete Framework Structure with Filenames", ""]

    for act in mapping.get("acts", []):
        act_num = act["number"]
        act_name = act["name"]
        total = counts.get(act["slug"], 0)
        lines.append(f"  Act {act_num}: {act_name} ({total} files)\n")

        for section in act.get("sections", []):
            sec_items = section.get("items", [])
            lines.append(f"  {section['code']} {section['name']} ({len(sec_items)} files)\n")

            # emit numbered filenames only (matches requested format)
            base_num = section['code']
            for idx, item in enumerate(sec_items, start=1):
                lines.append(f"  {base_num}.{idx} {item['filename']}")
            lines.append("")

        lines.append("  ---")

    content = "\n".join(lines) + "\n"
    # Write to project root (legacy) and to export folder (separate file as requested)
    MANIFEST.write_text(content, encoding="utf-8")
    ensure_dir(EXPORT)
    MANIFEST_EXPORT.write_text(content, encoding="utf-8")


def main():
    mapping = load_mapping()
    counts = export_from_mapping(mapping)
    write_manifest(mapping, counts)
    print(f"✅ Export complete → {EXPORT}")
    print(f"✅ Manifest written → {MANIFEST}")
    print(f"✅ Manifest written → {MANIFEST_EXPORT}")

    # Run validator for convenience (non-fatal)
    try:
        import importlib.util
        validator_path = ROOT / 'scripts' / 'validate_framework_export.py'
        spec = importlib.util.spec_from_file_location('validate_framework_export', str(validator_path))
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            rc = mod.main()
        else:
            raise RuntimeError('unable to import validator module')
        if rc == 0:
            print("✅ Validation: PASSED")
        else:
            print("❌ Validation: FAILED (see errors above)")
    except Exception as e:
        print(f"⚠️  Validation skipped: {e}")


if __name__ == "__main__":
    main()
