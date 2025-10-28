# Flyberry Brand Platform

[![CI Status](https://github.com/kalpeshjaju/flyberry_platform/workflows/Flyberry%20Platform%20CI/badge.svg)](https://github.com/kalpeshjaju/flyberry_platform/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This platform provides a unified, scalable, and testable system for generating and validating the Flyberry brand framework. It is built on a modular, block-based architecture where each step of the process is a self-contained, runnable unit.

## Core Concepts

- **Platform, Not a Script:** This isn't just a collection of scripts; it's a platform. The goal is to provide a stable foundation for repeatable, high-quality brand framework generation.
- **Blocks:** The core logic is organized into "blocks" inside the `blocks/` directory. Each block is responsible for one specific task (e.g., loading data, generating a framework, validating output).
- **Specs:** You define a pipeline by creating a `.yml` file in the `specs/` directory. This "spec" file declares which blocks to run, in what order, and with what configuration. This makes our process declarative, version-controllable, and easy to reproduce.
- **Fixtures:** All raw data, templates, and other assets required for a run are stored in the `fixtures/` directory. This keeps our logic separate from our data.

## Directory Structure

- `core/engine/`: Contains the central Python scripts that read specs, orchestrate execution, and render reports.
- `blocks/`: Contains the individual, self-contained logic units.
  - `data_loader/`: Loads and processes raw data from `fixtures/`.
  - `framework_generator/`: Generates the brand framework.
  - `validator/`: Validates the output of the generator.
- `specs/`: Contains the declarative YAML files that define pipelines.
- `fixtures/`: Contains all the data, templates, and assets needed to run the pipelines.
- `product/`: Contains the final, validated outputs of a successful run.
- `docs/`: Contains all project documentation.

## How to Run a Pipeline

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Define a Spec:**
    Create or modify a `.yml` file in the `specs/` directory. See `specs/generate-flyberry-framework.yml` for an example.

3.  **Execute the Pipeline (MVP spec):**
    ```bash
    python core/engine/run.py --spec specs/generate-flyberry-framework.yml
    ```

4.  **Run Blockized Sample Suites:**
    - Brand package (palette + tokens):
      ```bash
      python core/engine/run.py --spec specs/flyberry_brand.yml
      ```
    - Site restart (a11y + links):
      ```bash
      python core/engine/run.py --spec specs/flyberry_oct_restart.yml
      ```

    These produce a canonical run JSON under `product/runs/<suite>/run.json` and any selected report projections.

5.  **Validate Spec Before Running:**
    ```bash
    python core/engine/validate_spec.py --spec specs/flyberry_brand.yml
    ```
    Validates spec structure, block imports, input paths, output profiles, and gates. Exits with code 1 on errors.

6.  **Plan Execution (Dry-Run):**
    ```bash
    python core/engine/plan.py --spec specs/flyberry_brand.yml
    ```
    Shows a detailed execution plan: steps, inputs, outputs, blocks resolved, gates, and profiles. Exits 0 if executable, 1 if issues.

7.  **Render Reports from a Previous Run (Artifact Pinning - no re-run):**
    ```bash
    python core/engine/render.py --run product/runs/<suite>/run.json --profile developer.json
    python core/engine/render.py --run product/runs/<suite>/run.json --profile exec.csv
    python core/engine/render.py --run product/runs/<suite>/run.json --profile brand-guide.html
    ```

    Or use `--from-run` with `run.py` to skip execution and just render:
    ```bash
    python core/engine/run.py --spec specs/flyberry_brand.yml --from-run product/runs/flyberry_brand/run.json
    ```

## Features

### Core Features
- **Canonical schemas**: `schemas/audit_run.v1.json`, `schemas/brand_package.v1.json` describe the canonical shapes.
- **Plugin contract**: blocks can return structured `CheckResult[]` that the engine aggregates.
- **Reporters**: developer JSON, exec CSV (with proper CSV escaping), and brand guide HTML projection.
- **Readiness gates v2**: global and per-check thresholds; engine computes `overall_gate_status` (pass/fail).
- **Validation modes**: soft (warn), strict (exit on schema failure), or none.
- **Watch mode**: efficient filesystem watching with optional `watchdog` (fallback to polling).
- **Planning & validation**: enhanced CLI tools with glob support, profile validation, and clear exit codes.
- **Artifact pinning**: re-render reports from saved runs without re-scanning.

### Advanced Workflows

#### Schema Validation

By default, the engine validates the canonical run JSON against `schemas/audit_run.v1.json` in **soft mode** (warnings only).

- **Soft mode** (default): Warns on validation errors, continues execution
  ```bash
  python core/engine/run.py --spec specs/flyberry_brand.yml
  ```

- **Strict mode**: Exits with code 1 on validation errors
  ```bash
  python core/engine/run.py --spec specs/flyberry_brand.yml --strict-validate
  ```

- **No validation**: Skips schema validation entirely
  ```bash
  python core/engine/run.py --spec specs/flyberry_brand.yml --no-validate
  ```

#### Watch Mode

Watch mode monitors your spec, inputs, and blocks for changes and automatically re-runs the pipeline. Perfect for rapid iteration!

**With watchdog (recommended):**
```bash
# Install watchdog first for efficient watching
pip install 'watchdog>=4.0.1'

# Run with watch mode
python core/engine/run.py --spec specs/flyberry_brand.yml --watch
```

**Without watchdog (fallback to polling):**
```bash
# Watch mode works without watchdog, but uses polling
python core/engine/run.py --spec specs/flyberry_brand.yml --watch --interval 2.0
```

Watch mode monitors:
- The spec file itself
- All input files declared in pipeline steps
- The entire `blocks/` directory (for quick dev loops)

#### Artifact Pinning

Re-render reports from a saved run JSON without re-executing the pipeline. Useful for:
- Iterating on report templates
- Generating multiple output formats from one scan
- Reviewing historical runs

```bash
# Initial run (saves to product/runs/flyberry_brand/run.json)
python core/engine/run.py --spec specs/flyberry_brand.yml

# Re-render with different profiles (no re-scan)
python core/engine/render.py --run product/runs/flyberry_brand/run.json --profile exec.csv
python core/engine/render.py --run product/runs/flyberry_brand/run.json --profile brand-guide.html

# Or use --from-run with run.py
python core/engine/run.py --spec specs/flyberry_brand.yml --from-run product/runs/flyberry_brand/run.json
```

**Combine with watch mode** to iterate on reporters:
```bash
# Terminal 1: Watch mode on reporter code
python core/engine/run.py --spec specs/flyberry_brand.yml --from-run product/runs/flyberry_brand/run.json --watch
# Edit core/reporters/brand_guide_html.py → auto re-renders
```

#### Readiness Gates

Gates are post-run checks that validate your run meets quality thresholds. The engine evaluates gates and sets `meta.overall_gate_status` to `"pass"` or `"fail"`.

**Global gates** check aggregate metrics across all results:
```yaml
gates:
  - { type: global, metric: issues_critical, op: "==", value: 0 }
  - { type: global, metric: issues_major, op: "<=", value: 5 }
```

**Per-check gates** validate metrics for specific checks:
```yaml
gates:
  - { type: check, check_id: brand.palette-contrast, metric: pairs_failing, op: "==", value: 0 }
  - { type: check, check_id: site.a11y-scan, metric: errors_found, op: "<=", value: 3 }
```

**Supported operators**: `==`, `<=`, `>=`, `<`, `>`

**Global metrics**:
- `issues_total`: Total issue count
- `issues_critical`, `issues_major`, `issues_minor`, `issues_info`: By severity

**Per-check metrics**: Any metric returned in a check's `metrics` object.

**Example spec** (see `specs/flyberry_brand.yml`):
```yaml
gates:
  - { type: global, metric: issues_critical, op: "==", value: 0 }
  - { type: check, check_id: brand.palette-contrast, metric: pairs_failing, op: "==", value: 0 }
```

**Output**:
```
Readiness Gates:
  - issues_critical == 0 => 0 [ PASS ]
  - brand.palette-contrast.pairs_failing == 0 => 0 [ PASS ]

Overall gate status: PASS
```
