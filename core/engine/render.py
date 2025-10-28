import argparse
import json
import os
import sys
from typing import Any, Dict

# Add the project root to the Python path to allow for absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


def load_run(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Render projections from a canonical run JSON")
    parser.add_argument('--run', required=True, help='Path to canonical run.json')
    parser.add_argument('--profile', required=True, choices=['developer.json', 'exec.csv', 'brand-guide.html'])
    parser.add_argument('--out', required=False, help='Optional output file path')
    args = parser.parse_args()

    run = load_run(args.run)
    profile = args.profile
    out_path = args.out
    if not out_path:
        base_dir = os.path.dirname(args.run)
        fname = 'developer.json' if profile == 'developer.json' else ('exec.csv' if profile == 'exec.csv' else 'brand-guide.html')
        out_path = os.path.join(base_dir, fname)

    if profile == 'developer.json':
        from core.reporters.developer_json import render as dev_render
        content = dev_render(run)
    elif profile == 'exec.csv':
        from core.reporters.exec_csv import render as csv_render
        content = csv_render(run)
    else:
        from core.reporters.brand_guide_html import render as html_render
        content = html_render(run)

    with open(out_path, 'w') as f:
        f.write(content)
    print(f"Rendered {profile} -> {out_path}")


if __name__ == '__main__':
    main()

