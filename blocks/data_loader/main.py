# blocks/data_loader/main.py
import os
import json

def run(inputs, outputs):
    """
    Loads data from input directories and creates a single processed JSON file.
    For this MVP, we'll just simulate this by listing files.
    """
    print("  Executing data_loader block...")
    
    processed_data = {
        "source_files": [],
        "notes": "This is a simulated processed data file from the data_loader block."
    }

    for input_path in inputs:
        if os.path.isdir(input_path):
            for filename in os.listdir(input_path):
                processed_data["source_files"].append(os.path.join(input_path, filename))
        elif os.path.isfile(input_path):
            processed_data["source_files"].append(input_path)

    # Write to the first specified output file
    if outputs:
        output_file = outputs[0]
        with open(output_file, 'w') as f:
            json.dump(processed_data, f, indent=2)
        print(f"  -> Data loader processed {len(processed_data['source_files'])} files.")
    else:
        print("  Warning: No outputs defined for data_loader.")

if __name__ == '__main__':
    # This allows the script to be run standalone for testing, though the
    # platform engine is the intended execution method.
    run(['fixtures/raw_data', 'fixtures/brand_intel'], ['product/processed_data.json'])
