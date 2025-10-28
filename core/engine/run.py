# core/engine/run.py
import yaml
import argparse
import importlib
import os
import sys
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

try:
    from jsonschema import validate as jsonschema_validate
    from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
except Exception:
    jsonschema_validate = None
    JsonSchemaValidationError = Exception

# Optional watchdog for efficient watch mode
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

# Add the project root to the Python path to allow for absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _aggregate_gate_metrics(results: List[Dict[str, Any]]) -> Dict[str, int]:
    metrics = {
        "issues_total": 0,
        "issues_critical": 0,
        "issues_major": 0,
        "issues_minor": 0,
        "issues_info": 0,
    }
    for r in results:
        for issue in r.get("issues", []) or []:
            metrics["issues_total"] += 1
            sev = (issue.get("severity") or "").lower()
            if sev in ("critical", "major", "minor", "info"):
                metrics[f"issues_{sev}"] += 1
    return metrics


def _load_yaml(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def _load_json(path: str) -> Any:
    with open(path, 'r') as f:
        return json.load(f)


def _load_schema(rel_path: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'schemas', rel_path)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None


def execute_pipeline(spec_path, from_run: Optional[str] = None, validate_schema: str = "soft"):
    """
    Parses and executes a pipeline defined in a spec YAML file.
    """
    print(f"--- Flyberry Platform Engine Initialized ---")
    print(f"Loading spec from: {spec_path}\n")

    try:
        spec = _load_yaml(spec_path)
    except FileNotFoundError:
        print(f"Error: Spec file not found at {spec_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML spec file: {e}")
        sys.exit(1)

    suite = spec.get('suite', 'default-suite')
    print(f"Successfully loaded suite: '{suite}'")
    print(f"Description: {spec.get('description', 'N/A')}\n")

    # Ensure the product directory exists
    if not os.path.exists('product'):
        os.makedirs('product')
        print("Created 'product/' directory for outputs.")
    runs_dir = os.path.join('product', 'runs', suite)
    _ensure_dir(runs_dir)

    pipeline = spec.get('pipeline', [])
    if not pipeline:
        print("Warning: Spec file contains an empty pipeline. Nothing to run.")
        return

    start_time = datetime.now()
    print(f"--- Starting Pipeline Execution at {start_time.strftime('%Y-%m-%d %H:%M:%S')} ---")

    run_record: Dict[str, Any] = {
        "run": {
            "id": f"run_{int(start_time.timestamp())}",
            "suite": suite,
            "started_at": _now_iso(),
            "schema_version": "1.0.0",
        },
        "requested_checks": [],
        "blocks_used": [],
        "results": [],
        "meta": {},
    }

    # If artifact pinning is requested, skip execution and reuse an existing run
    if from_run:
        try:
            run_record = _load_json(from_run)
        except Exception as e:
            print(f"Error: Failed to load pinned run from {from_run}: {e}")
            sys.exit(1)
    else:
        for i, step in enumerate(pipeline):
            step_name = step.get('name', f'step_{i+1}')
            block_name = step.get('block')
            inputs = step.get('inputs', [])
            outputs = step.get('outputs', [])

            print(f"\n[{i+1}/{len(pipeline)}] Running Block: '{block_name}' (Step: '{step_name}')")
            print(f"  Description: {step.get('description', 'No description.')}")
            
            if not block_name:
                print("  Error: 'block' not defined for this step. Skipping.")
                continue

            try:
                # Dynamically import the block's main module
                module_path = f"blocks.{block_name}.main"
                block_module = importlib.import_module(module_path)
                
                # Call the block's run function
                result = block_module.run(inputs, outputs)
                
                print(f"  Block '{block_name}' executed successfully.")
                if outputs:
                    for output in outputs:
                        print(f"  -> Created output: {output}")

                # Aggregate structured results if provided
                if isinstance(result, dict):
                    block_id = result.get("block_id")
                    if block_id and block_id not in run_record["blocks_used"]:
                        run_record["blocks_used"].append(block_id)
                    for cr in result.get("check_results", []) or []:
                        # collect requested checks list
                        cid = cr.get("check_id")
                        if cid and cid not in run_record["requested_checks"]:
                            run_record["requested_checks"].append(cid)
                        run_record["results"].append(cr)
                    # Optional: merge suggested meta from blocks
                    if isinstance(result.get("meta"), dict):
                        run_record["meta"].update(result.get("meta", {}))

            except ImportError:
                print(f"  Error: Could not find or import module for block '{block_name}'.")
                print(f"  Please ensure 'blocks/{block_name}/main.py' exists.")
            except Exception as e:
                print(f"  Error: An exception occurred while running block '{block_name}': {e}")
                # In a real implementation, you might want to stop the pipeline here.
                # For the MVP, we will continue.

    # Schema validation (optional) and persist canonical run JSON if results were produced
    if run_record["results"]:
        validation_failed = False
        if validate_schema in ("soft", "strict") and jsonschema_validate is not None:
            schema = _load_schema('audit_run.v1.json')
            if schema:
                try:
                    jsonschema_validate(instance=run_record, schema=schema)
                    print("✓ Schema validation passed")
                except JsonSchemaValidationError as ve:
                    validation_failed = True
                    msg = f"Schema validation failed: {ve}"
                    if validate_schema == "strict":
                        print(f"Error: {msg}")
                        sys.exit(1)
                    else:
                        print(f"Warning: {msg}")
            else:
                print("Warning: audit_run.v1.json schema not found; skipping validation.")

        # Evaluate simple readiness gates, if any (global counts)
        gates = spec.get('gates', []) or []
        gate_results = []
        if gates:
            print("\nReadiness Gates:")
            counts = _aggregate_gate_metrics(run_record["results"])
            # quick index results by check_id for metric gates
            by_check: Dict[str, Dict[str, Any]] = {}
            for r in run_record["results"]:
                by_check[r.get('check_id','')] = r
            for g in gates:
                gtype = g.get('type', 'global')
                op = g.get('op')
                val = g.get('value')
                if op not in ("==", "<=", ">=", "<", ">"):
                    print(f"  - Skipped invalid gate op: {g}")
                    continue
                if gtype == 'global':
                    metric = g.get('metric')
                    if metric not in counts:
                        print(f"  - Skipped unknown global metric: {metric}")
                        continue
                    lhs = counts[metric]
                    ok = ((op == "==" and lhs == val) or (op == "<=" and lhs <= val) or (op == ">=" and lhs >= val) or (op == "<" and lhs < val) or (op == ">" and lhs > val))
                    gate_results.append(ok)
                    print(f"  - {metric} {op} {val} => {lhs} [{ 'PASS' if ok else 'FAIL' }]")
                elif gtype == 'check':
                    cid = g.get('check_id')
                    metric = g.get('metric')
                    r = by_check.get(cid)
                    if not r or 'metrics' not in r or metric not in r['metrics']:
                        print(f"  - Skipped check gate (missing): {cid}.{metric}")
                        continue
                    lhs = r['metrics'][metric]
                    ok = ((op == "==" and lhs == val) or (op == "<=" and lhs <= val) or (op == ">=" and lhs >= val) or (op == "<" and lhs < val) or (op == ">" and lhs > val))
                    gate_results.append(ok)
                    print(f"  - {cid}.{metric} {op} {val} => {lhs} [{ 'PASS' if ok else 'FAIL' }]")
                else:
                    print(f"  - Skipped unknown gate type: {gtype}")

        # Compute overall gate status
        overall_gate_status = "pass" if (not gate_results or all(gate_results)) else "fail"
        run_record["meta"]["overall_gate_status"] = overall_gate_status

        run_path = os.path.join(runs_dir, 'run.json')
        with open(run_path, 'w') as f:
            json.dump(run_record, f, indent=2)
        print(f"\nCanonical run JSON written: {run_path}")
        print(f"Overall gate status: {overall_gate_status.upper()}")

        # Render projections if requested
        output = spec.get('output', {}) or {}
        profiles = output.get('profiles', []) or []
        for profile in profiles:
            try:
                if profile == 'developer.json':
                    from core.reporters.developer_json import render as dev_render
                    content = dev_render(run_record)
                    out_path = os.path.join(runs_dir, 'developer.json')
                    with open(out_path, 'w') as f:
                        f.write(content)
                    print(f"  Rendered: {out_path}")
                elif profile == 'exec.csv':
                    from core.reporters.exec_csv import render as csv_render
                    content = csv_render(run_record)
                    out_path = os.path.join(runs_dir, 'exec.csv')
                    with open(out_path, 'w') as f:
                        f.write(content)
                    print(f"  Rendered: {out_path}")
                elif profile == 'brand-guide.html':
                    from core.reporters.brand_guide_html import render as html_render
                    content = html_render(run_record)
                    out_path = os.path.join(runs_dir, 'brand-guide.html')
                    with open(out_path, 'w') as f:
                        f.write(content)
                    print(f"  Rendered: {out_path}")
            except Exception as re:
                print(f"  Warning: Failed to render profile '{profile}': {re}")

    end_time = datetime.now()
    print(f"\n--- Pipeline Execution Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    print(f"Total execution time: {end_time - start_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flyberry Platform Execution Engine")
    parser.add_argument('--spec', required=True, help="Path to the pipeline spec YAML file.")
    parser.add_argument('--from-run', required=False, help="Path to a prior canonical run.json (artifact pinning).")
    parser.add_argument('--no-validate', action='store_true', help="Skip JSON schema validation of run output.")
    parser.add_argument('--strict-validate', action='store_true', help="Enable strict schema validation (exit on failure).")
    parser.add_argument('--watch', action='store_true', help="Watch spec and fixtures for changes and re-run.")
    parser.add_argument('--interval', type=float, default=1.0, help="Watch interval in seconds (polling mode).")
    args = parser.parse_args()

    # Determine validation mode
    if args.no_validate:
        validation_mode = "none"
    elif args.strict_validate:
        validation_mode = "strict"
    else:
        validation_mode = "soft"

    def _collect_watch_paths(spec_path: str, spec: Dict[str, Any]) -> Set[str]:
        paths: Set[str] = {spec_path}
        for step in spec.get('pipeline', []):
            for p in step.get('inputs', []) or []:
                if isinstance(p, str) and os.path.exists(p):
                    paths.add(p)
        # always include blocks directory for quick dev loops
        paths.add(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'blocks'))
        return paths

    if not args.watch:
        execute_pipeline(args.spec, from_run=args.from_run, validate_schema=validation_mode)
    else:
        spec = _load_yaml(args.spec)
        paths = _collect_watch_paths(args.spec, spec)

        if HAS_WATCHDOG:
            print("Watch mode enabled (using watchdog). Press Ctrl+C to stop.")

            class ChangeHandler(FileSystemEventHandler):
                def __init__(self):
                    self.debounce_time = 0.5
                    self.last_triggered = 0

                def on_any_event(self, event):
                    import time
                    now = time.time()
                    if now - self.last_triggered > self.debounce_time:
                        self.last_triggered = now
                        print(f"\nChange detected: {event.src_path}. Re-running...")
                        execute_pipeline(args.spec, from_run=args.from_run, validate_schema=validation_mode)

            observer = Observer()
            handler = ChangeHandler()

            for p in paths:
                if os.path.isdir(p):
                    observer.schedule(handler, p, recursive=True)
                elif os.path.isfile(p):
                    observer.schedule(handler, os.path.dirname(p), recursive=False)

            observer.start()
            execute_pipeline(args.spec, from_run=args.from_run, validate_schema=validation_mode)

            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                observer.join()
                print("\nStopped watch mode.")
        else:
            print("Watch mode enabled (polling, install watchdog for better performance). Press Ctrl+C to stop.")
            try:
                import time
                mtimes: Dict[str, float] = {}
                def snapshot() -> Dict[str, float]:
                    snap: Dict[str, float] = {}
                    for p in list(paths):
                        if os.path.isdir(p):
                            for root, _dirs, files in os.walk(p):
                                for fn in files:
                                    fp = os.path.join(root, fn)
                                    try:
                                        snap[fp] = os.path.getmtime(fp)
                                    except Exception:
                                        pass
                        elif os.path.isfile(p):
                            try:
                                snap[p] = os.path.getmtime(p)
                            except Exception:
                                pass
                    return snap
                mtimes = snapshot()
                execute_pipeline(args.spec, from_run=args.from_run, validate_schema=validation_mode)
                while True:
                    time.sleep(args.interval)
                    new_snap = snapshot()
                    if new_snap != mtimes:
                        mtimes = new_snap
                        print("\nChange detected. Re-running...")
                        execute_pipeline(args.spec, from_run=args.from_run, validate_schema=validation_mode)
            except KeyboardInterrupt:
                print("\nStopped watch mode.")
