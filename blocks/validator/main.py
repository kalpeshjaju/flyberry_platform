# blocks/validator/main.py
import os

def run(inputs, outputs):
    """
    Validates the generated brand framework.
    """
    print("  Executing validator block...")

    # Check the first input file
    if not inputs:
        print("  Error: No input file specified for validation.")
        return

    framework_file = inputs[0]
    if not os.path.exists(framework_file):
        print(f"  Error: Framework file '{framework_file}' not found for validation.")
        return

    with open(framework_file, 'r') as f:
        content = f.read()

    # Simple validation rules for the MVP
    errors = []
    if "Flyberry Brand Framework" not in content:
        errors.append("Missing title: 'Flyberry Brand Framework'")
    if "Processed Data Summary" not in content:
        errors.append("Missing section: 'Processed Data Summary'")
    if len(content) < 100:
        errors.append(f"Content too short (only {len(content)} characters).")

    if not errors:
        print("  Validation PASSED: All checks met.")
    else:
        print(f"  Validation FAILED: Found {len(errors)} issues.")
        for error in errors:
            print(f"    - {error}")
    
    # This block doesn't produce a file, it just prints to console.
    # A real implementation might produce a validation_report.json.

if __name__ == '__main__':
    run(['product/flyberry_brand_framework.md'], [])