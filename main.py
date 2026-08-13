import os 
import json
import sys
sys.path.insert(0, os.path.abspath("src"))
from ijazah_parser.pipeline import process_directory

def main():
    input_dir = os.path.join("data", "raw")
    output_dir = os.path.join("data", "processed")
    output_file = os.path.join(output_dir, "extraction_results.json")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Scanning '{input_dir}' for the files...")
    results = process_directory(input_dir, is_transcript=False)
    if not results:
        print("No compatible files found.")
        return
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Processed {len(results)} files succesfully.")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()
