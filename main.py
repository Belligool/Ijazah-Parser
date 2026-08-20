import os
import sys
sys.path.insert(0, os.path.abspath("src"))
from ijazah_parser.pipeline import *

if __name__ == "__main__":
    folder_to_scan = "data/raw"
    output_folder = os.path.join("data", "processed")
    output_file = os.path.join(output_folder, "extraction_results.xlsx")
    os.makedirs(output_folder, exist_ok=True)
    extraction_results = process_directory(folder_to_scan)
    export_to_excel(extraction_results, output_file)
