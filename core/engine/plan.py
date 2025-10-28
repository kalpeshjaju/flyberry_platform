import argparse
import importlib
import json
import os
import sys
import yaml
from typing import Any, Dict, List


KNOWN_PROFILES = ["developer.json", "exec.csv", "brand-guide.html"]


def load_spec(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def generate_plan(spec_path: str, project_root: str) -> Dict[str, Any]:
    """Generate execution plan from a spec."""
    try:
        spec = load_spec(spec_path)
    except Exception as e:
        return {
            "executable": False,
            "error": f"Failed to parse spec YAML: {e}",
            "spec_path": os.path.relpath(spec_path, project_root)
        }

    suite = spec.get('suite', 'default')
    description = spec.get('description', 'N/A')
    pipeline = spec.get('pipeline', [])
    gates = spec.get('gates', []) or []
    profiles = (spec.get('output', {}) or {}).get('profiles', [])

    plan = {
        "executable": True,
        "spec_path": os.path.relpath(spec_path, project_root),
        "suite": suite,
        "description": description,
        "steps": [],
        "summary": {
            "total_steps": len(pipeline),
            "total_inputs": 0,
            "total_outputs": 0,
            "blocks_resolved": [],
            "blocks_missing": [],
            "gates": len(gates),
            "profiles": profiles,
            "unknown_profiles": []
        },
        "gates": [],
        "issues": []
    }

    if not pipeline:
        plan["issues"].append("Empty pipeline. Nothing to execute.")
        plan["executable"] = True  # Not an error, just a warning
        return plan

    # Process each step
    for i, step in enumerate(pipeline):
        step_name = step.get('name', f'step_{i+1}')
        block_name = step.get('block')
        step_desc = step.get('description', '')
        inputs = step.get('inputs', []) or []
        outputs = step.get('outputs', []) or []

        plan["summary"]["total_inputs"] += len(inputs)
        plan["summary"]["total_outputs"] += len(outputs)

        step_info = {
            "index": i + 1,
            "name": step_name,
            "block": block_name,
            "description": step_desc,
            "module_status": "ok",
            "inputs": [],
            "outputs": []
        }

        # Module existence check
        try:
            importlib.import_module(f"blocks.{block_name}.main")
            plan["summary"]["blocks_resolved"].append(block_name)
        except Exception as e:
            step_info["module_status"] = "missing"
            step_info["module_error"] = str(e)
            plan["summary"]["blocks_missing"].append(block_name)
            plan["issues"].append(f"Step[{i}]: cannot import blocks.{block_name}.main ({e})")
            plan["executable"] = False

        # Check inputs
        for inp in inputs:
            inp_path = inp if os.path.isabs(inp) else os.path.join(project_root, inp)
            inp_info = {"path": inp}

            if '*' in inp or '?' in inp:
                inp_info["status"] = "glob_pattern"
            elif os.path.exists(inp_path):
                inp_info["status"] = "exists"
            else:
                inp_info["status"] = "missing"
                plan["issues"].append(f"Step[{i}]: input path missing -> {inp}")
                plan["executable"] = False

            step_info["inputs"].append(inp_info)

        # Outputs
        step_info["outputs"] = outputs

        plan["steps"].append(step_info)

    # Process gates
    for i, gate in enumerate(gates):
        gtype = gate.get('type', 'global')
        gate_info = {
            "index": i + 1,
            "type": gtype
        }

        if gtype == 'global':
            gate_info["metric"] = gate.get('metric', '?')
            gate_info["op"] = gate.get('op', '?')
            gate_info["value"] = gate.get('value', '?')
        elif gtype == 'check':
            gate_info["check_id"] = gate.get('check_id', '?')
            gate_info["metric"] = gate.get('metric', '?')
            gate_info["op"] = gate.get('op', '?')
            gate_info["value"] = gate.get('value', '?')
        else:
            gate_info["type"] = "unknown"

        plan["gates"].append(gate_info)

    # Check profiles
    unknown_profiles = [p for p in profiles if p not in KNOWN_PROFILES]
    plan["summary"]["unknown_profiles"] = unknown_profiles
    if unknown_profiles:
        plan["issues"].append(f"Unknown profiles: {', '.join(unknown_profiles)}")
        plan["executable"] = False

    return plan


def print_human_readable(plan: Dict[str, Any]):
    """Print plan in human-readable format."""
    print("=" * 60)
    print(f"EXECUTION PLAN: {plan.get('suite', 'N/A')}")
    print("=" * 60)
    print(f"Description: {plan.get('description', 'N/A')}")
    print(f"Spec: {plan['spec_path']}\n")

    if plan.get("error"):
        print(f"❌ Error: {plan['error']}")
        return False

    summary = plan["summary"]
    steps = plan["steps"]

    if not steps:
        print("⚠ Warning: Empty pipeline. Nothing to execute.")
        return True

    print(f"Pipeline Steps: {summary['total_steps']}")
    print("-" * 60)

    # Print steps
    for step in steps:
        print(f"\n[{step['index']}] {step['name']}")
        print(f"    Block: {step['block']}")
        if step.get('description'):
            print(f"    Description: {step['description']}")

        # Module status
        if step['module_status'] == 'ok':
            print(f"    Module status: ✓ OK")
        else:
            print(f"    Module status: ✗ MISSING ({step.get('module_error', '')})")

        # Inputs
        if step['inputs']:
            print(f"    Inputs ({len(step['inputs'])}):")
            for inp in step['inputs']:
                status = inp['status']
                if status == 'exists':
                    status_str = "✓"
                elif status == 'glob_pattern':
                    status_str = "(glob pattern)"
                else:
                    status_str = "✗ missing"
                print(f"      - {inp['path']} {status_str}")

        # Outputs
        if step['outputs']:
            print(f"    Outputs ({len(step['outputs'])}):")
            for out in step['outputs']:
                print(f"      - {out}")

    # Gates
    if plan['gates']:
        print(f"\n{'-' * 60}")
        print(f"Gates ({len(plan['gates'])}):")
        for gate in plan['gates']:
            if gate['type'] == 'global':
                print(f"  [{gate['index']}] {gate['type']}: {gate['metric']} {gate['op']} {gate['value']}")
            elif gate['type'] == 'check':
                print(f"  [{gate['index']}] {gate['type']}: {gate['check_id']}.{gate['metric']} {gate['op']} {gate['value']}")
            else:
                print(f"  [{gate['index']}] unknown type: {gate['type']}")

    # Summary
    print(f"\n{'-' * 60}")
    print("Summary:")
    print(f"  Steps: {summary['total_steps']}")
    print(f"  Inputs: {summary['total_inputs']}")
    print(f"  Outputs: {summary['total_outputs']}")
    print(f"  Blocks resolved: {len(summary['blocks_resolved'])}")
    if summary['blocks_missing']:
        print(f"  Blocks missing: {len(summary['blocks_missing'])} ({', '.join(summary['blocks_missing'])})")
    print(f"  Gates: {summary['gates']}")

    profiles = summary['profiles']
    unknown = summary['unknown_profiles']
    if profiles:
        print(f"  Output profiles: {', '.join(profiles)}")
        if unknown:
            print(f"    ⚠ Unknown profiles: {', '.join(unknown)}")
    else:
        print(f"  Output profiles: none")

    print("=" * 60)

    if plan['executable']:
        print("✅ Plan is executable. All dependencies resolved.")
        return True
    else:
        print("❌ Plan has issues. Fix errors before running.")
        return False


def print_json_output(plan: Dict[str, Any]):
    """Print plan in JSON format."""
    print(json.dumps(plan, indent=2))
    return plan.get('executable', False)


def main():
    parser = argparse.ArgumentParser(description="Plan the execution for a spec (dry-run)")
    parser.add_argument('--spec', required=True, help='Spec YAML path')
    parser.add_argument('--json', action='store_true', help='Output JSON for machine parsing')
    args = parser.parse_args()

    # Add project root to import path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, project_root)

    # Resolve relative spec path
    spec_path = args.spec if os.path.isabs(args.spec) else os.path.join(project_root, args.spec)
    if not os.path.exists(spec_path):
        if args.json:
            print(json.dumps({
                "executable": False,
                "error": f"Spec file not found: {args.spec}",
                "spec_path": args.spec
            }))
        else:
            print(f"Error: Spec file not found: {args.spec}")
        sys.exit(1)

    # Generate plan
    plan = generate_plan(spec_path, project_root)

    # Output plan
    if args.json:
        executable = print_json_output(plan)
    else:
        executable = print_human_readable(plan)

    sys.exit(0 if executable else 1)


if __name__ == '__main__':
    main()
