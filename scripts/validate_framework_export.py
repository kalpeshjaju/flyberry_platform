#!/usr/bin/env python3
"""
Validate framework_export against framework_mapping.yaml.

Checks:
- Every mapped item exists in framework_export in the expected path
- Required fields present in each JSON item
- Section-level counts match mapping
- Emits a summary and exits non-zero on failure (CI-friendly)
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "framework_export"
MAPPING = ROOT / "framework_mapping.yaml"


REQUIRED_FIELDS = ["title", "source_hint", "status", "lineage"]
REQUIRED_LINEAGE_FIELDS = ["type"]


def load_mapping() -> dict:
    return yaml.safe_load(MAPPING.read_text(encoding="utf-8"))


def validate_item_json(path: Path) -> List[str]:
    errs: List[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"Invalid JSON: {path}: {e}"]

    for k in REQUIRED_FIELDS:
        if k not in data:
            errs.append(f"Missing field '{k}' in {path}")

    lineage = data.get("lineage", {}) or {}
    for k in REQUIRED_LINEAGE_FIELDS:
        if k not in lineage:
            errs.append(f"Missing lineage.{k} in {path}")

    status = data.get("status")
    if status not in ("draft", "todo", "complete"):
        errs.append(f"Invalid status '{status}' in {path}")

    return errs


def main() -> int:
    mapping = load_mapping()
    total_expected = 0
    total_found = 0
    errors: List[str] = []

    for act in mapping.get("acts", []):
        act_dir = EXPORT / act["slug"]
        if not act_dir.exists():
            errors.append(f"Missing act directory: {act_dir}")
            continue

        for section in act.get("sections", []):
            section_dir = act_dir / section["slug"]
            if not section_dir.exists():
                errors.append(f"Missing section directory: {section_dir}")
                continue

            expected = section.get("items", [])
            total_expected += len(expected)
            found_count = 0

            for item in expected:
                p = section_dir / item["filename"]
                if not p.exists():
                    errors.append(f"Missing item file: {p}")
                    continue
                found_count += 1
                total_found += 1
                errors.extend(validate_item_json(p))

            # count check
            actual_files = [f for f in section_dir.glob("*") if f.is_file()]
            # There may be non-item files (STRUCTURE.md), so we only count expected
            if found_count != len(expected):
                errors.append(
                    f"Count mismatch in {section_dir}: expected {len(expected)}, found {found_count}"
                )

    # Summary
    print(f"Expected items: {total_expected}")
    print(f"Found items:    {total_found}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"- {e}")
        print(f"\nValidation FAILED with {len(errors)} error(s).")
        return 1
    else:
        print("\nValidation PASSED.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

