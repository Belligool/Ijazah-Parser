import os 
import json
import sys
import time
sys.path.insert(0, os.path.abspath("src"))
from ijazah_parser.pipeline import *

def main():
    start_time = time.perf_counter()
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
    end_time = time.perf_counter()
    total_seconds = end_time - start_time
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Processed {len(results)} files succesfully in {int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds.")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    folder_to_scan = "data/raw"
    output_folder = os.path.join("data", "processed")
    output_file = os.path.join(output_folder, "extraction_results.xlsx")
    os.makedirs(output_folder, exist_ok=True)
    print("Starting pipeline...")
    extraction_results = process_directory(folder_to_scan)
    export_to_excel(extraction_results, output_file)
