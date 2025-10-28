import argparse
import glob as glob_module
import importlib
import json
import os
import sys
import yaml
from typing import Any, Dict, List

try:
    from jsonschema import validate as jsonschema_validate, ValidationError as JsonSchemaValidationError
except ImportError:
    jsonschema_validate = None
    JsonSchemaValidationError = Exception


KNOWN_PROFILES = ["developer.json", "exec.csv", "brand-guide.html"]


def load_spec(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def load_schema(project_root: str, rel_path: str) -> Any:
    path = os.path.join(project_root, 'schemas', rel_path)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None


def validate_single_spec(spec_path: str, project_root: str) -> Dict[str, Any]:
    """Validate a single spec and return structured results."""
    result = {
        "path": os.path.relpath(spec_path, project_root),
        "absolute_path": spec_path,
        "valid": True,
        "errors": [],
        "suite": None,
        "blocks": [],
        "gates": 0,
        "profiles": [],
        "steps": 0,
        "inputs": 0,
        "outputs": 0
    }

    try:
        spec = load_spec(spec_path)
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Failed to parse YAML: {e}")
        return result

    # Basic structure validation
    if 'suite' not in spec:
        result["errors"].append("missing: suite")
        result["valid"] = False
    else:
        result["suite"] = spec['suite']

    if 'pipeline' not in spec or not isinstance(spec.get('pipeline'), list):
        result["errors"].append("missing: pipeline[] (must be an array)")
        result["valid"] = False
    else:
        result["steps"] = len(spec.get('pipeline', []))

    # Validate spec shape with schema if available
    if jsonschema_validate:
        spec_schema = {
            "type": "object",
            "required": ["suite", "pipeline"],
            "properties": {
                "suite": {"type": "string"},
                "pipeline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["block"],
                        "properties": {
                            "name": {"type": "string"},
                            "block": {"type": "string"},
                            "description": {"type": "string"},
                            "inputs": {"type": "array"},
                            "outputs": {"type": "array"}
                        }
                    }
                },
                "gates": {"type": "array"},
                "output": {
                    "type": "object",
                    "properties": {
                        "profiles": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        }
        try:
            jsonschema_validate(instance=spec, schema=spec_schema)
        except JsonSchemaValidationError as ve:
            result["errors"].append(f"spec shape invalid: {ve.message}")
            result["valid"] = False

    # Validate pipeline steps
    for i, step in enumerate(spec.get('pipeline', [])):
        if 'block' not in step:
            result["errors"].append(f"step[{i}]: missing 'block' field")
            result["valid"] = False
            continue

        block_name = step['block']
        result["blocks"].append(block_name)

        # Check if block module exists
        try:
            importlib.import_module(f"blocks.{block_name}.main")
        except Exception as e:
            result["errors"].append(f"step[{i}]: cannot import blocks.{block_name}.main ({e})")
            result["valid"] = False

        # Count and validate inputs
        inputs = step.get('inputs', []) or []
        result["inputs"] += len(inputs)
        for ip in inputs:
            if not isinstance(ip, str):
                continue
            # Skip glob patterns (they're resolved at runtime)
            if '*' in ip or '?' in ip:
                continue
            # Resolve relative to project root
            p = ip if os.path.isabs(ip) else os.path.join(project_root, ip)
            if not os.path.exists(p):
                result["errors"].append(f"step[{i}]: input path missing -> {ip}")
                result["valid"] = False

        # Count outputs
        outputs = step.get('outputs', []) or []
        result["outputs"] += len(outputs)

    # Validate output profiles
    profiles = (spec.get('output', {}) or {}).get('profiles', [])
    result["profiles"] = profiles
    if profiles:
        for profile in profiles:
            if profile not in KNOWN_PROFILES:
                result["errors"].append(f"output.profiles: unknown profile '{profile}' (known: {', '.join(KNOWN_PROFILES)})")
                result["valid"] = False

    # Validate gates
    gates = spec.get('gates', [])
    result["gates"] = len(gates)
    if gates:
        for i, gate in enumerate(gates):
            gtype = gate.get('type', 'global')
            if gtype not in ('global', 'check'):
                result["errors"].append(f"gates[{i}]: unknown type '{gtype}' (must be 'global' or 'check')")
                result["valid"] = False
            if 'op' not in gate or gate['op'] not in ("==", "<=", ">=", "<", ">"):
                result["errors"].append(f"gates[{i}]: invalid or missing 'op' (must be ==, <=, >=, <, >)")
                result["valid"] = False
            if 'value' not in gate:
                result["errors"].append(f"gates[{i}]: missing 'value'")
                result["valid"] = False
            if gtype == 'global' and 'metric' not in gate:
                result["errors"].append(f"gates[{i}]: global gate missing 'metric'")
                result["valid"] = False
            if gtype == 'check' and ('check_id' not in gate or 'metric' not in gate):
                result["errors"].append(f"gates[{i}]: check gate missing 'check_id' or 'metric'")
                result["valid"] = False

    return result


def print_human_readable(results: List[Dict[str, Any]], project_root: str):
    """Print validation results in human-readable format."""
    all_valid = True
    for result in results:
        print(f"\n{'='*60}")
        print(f"Validating: {result['path']}")
        print(f"{'='*60}")

        if not result["valid"]:
            all_valid = False

        # Show successful checks
        if result["valid"] or len(result["errors"]) < len([1,2,3,4]):  # Not all checks failed
            if result["suite"]:
                print(f"✓ Suite: {result['suite']}")
            if result["steps"] > 0:
                print("✓ Spec structure is valid")
            if result["blocks"]:
                for i, block in enumerate(result["blocks"]):
                    if not any(f"step[{i}]" in e and "cannot import" in e for e in result["errors"]):
                        print(f"✓ Step[{i}] block '{block}' module found")
            if result["profiles"] and not any("unknown profile" in e for e in result["errors"]):
                print(f"✓ Output profiles valid: {', '.join(result['profiles'])}")
            if result["gates"] > 0 and not any("gates" in e for e in result["errors"]):
                print(f"✓ Gates are valid ({result['gates']} gates)")

        # Show errors
        if result["errors"]:
            print(f"\n❌ Spec INVALID ({len(result['errors'])} errors):")
            for e in result["errors"]:
                print(f"  - {e}")
        else:
            print("\n✅ Spec OK")

    # Summary
    if not all_valid:
        print(f"\n{'='*60}")
        print(f"❌ {sum(1 for r in results if not r['valid'])} spec(s) failed validation")
        print(f"{'='*60}")
        return False
    else:
        print(f"\n{'='*60}")
        print(f"✅ All specs valid ({len(results)} spec(s))")
        print(f"{'='*60}")
        return True


def print_json_output(results: List[Dict[str, Any]]):
    """Print validation results in JSON format."""
    output = {
        "valid": all(r["valid"] for r in results),
        "total_specs": len(results),
        "valid_specs": sum(1 for r in results if r["valid"]),
        "invalid_specs": sum(1 for r in results if not r["valid"]),
        "specs": results
    }
    print(json.dumps(output, indent=2))
    return output["valid"]


def main():
    parser = argparse.ArgumentParser(description="Validate spec structure and references")
    parser.add_argument('--spec', required=True, help='Spec YAML path (supports glob patterns)')
    parser.add_argument('--json', action='store_true', help='Output JSON for machine parsing')
    args = parser.parse_args()

    # Add project root to import path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, project_root)

    # Resolve glob patterns in spec path
    spec_paths = []
    if '*' in args.spec or '?' in args.spec:
        spec_paths = glob_module.glob(args.spec)
        if not spec_paths:
            if args.json:
                print(json.dumps({"valid": False, "error": f"No specs matched pattern: {args.spec}"}))
            else:
                print(f"Error: No specs matched pattern: {args.spec}")
            sys.exit(1)
    else:
        # Resolve relative paths against repo root
        spec_path = args.spec if os.path.isabs(args.spec) else os.path.join(project_root, args.spec)
        if not os.path.exists(spec_path):
            if args.json:
                print(json.dumps({"valid": False, "error": f"Spec file not found: {args.spec}"}))
            else:
                print(f"Error: Spec file not found: {args.spec}")
            sys.exit(1)
        spec_paths = [spec_path]

    # Validate all specs
    results = [validate_single_spec(path, project_root) for path in spec_paths]

    # Output results
    if args.json:
        all_valid = print_json_output(results)
    else:
        all_valid = print_human_readable(results, project_root)

    sys.exit(0 if all_valid else 1)


if __name__ == '__main__':
    main()
