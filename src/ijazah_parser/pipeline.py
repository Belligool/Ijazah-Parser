import os
import glob
import tempfile
import cv2
from typing import Dict, Any, List
from pydantic import ValidationError
from pdf2image import convert_from_path
from ijazah_parser.preprocessing import remove_guilloche_background, apply_adaptive_thresholding
from ijazah_parser.ocr import extract_text_from_image
from ijazah_parser.extractors import extract_biodata, extract_pin_sivil, extract_ijazah_sekolah, extract_ipk, extract_transcript_rows
from ijazah_parser.validators import IjazahRecord, BiodataSchema, AcademicSchema

def process_single_image(image_path: str, is_transcript: bool = False) -> Dict[str, any]:
    clean_image = remove_guilloche_background(image_path)
    binary_image = apply_adaptive_thresholding(clean_image)
    debug_img_name = f"debug_{os.path.basename(image_path)}"
    cv2.imwrite(os.path.join("data", "samples", debug_img_name), binary_image)
    ocr_text, avg_confidence = extract_text_from_image(binary_image)
    print(f"\n--- RAW OCR FOR {os.path.basename(image_path)} ---")
    print(ocr_text)
    print("--------------------------------------------------\n")
    biodata = extract_biodata(ocr_text)
    nomor_ijazah = extract_pin_sivil(ocr_text)
    if not nomor_ijazah:
        nomor_ijazah = extract_ijazah_sekolah(ocr_text)
    akademik = AcademicSchema(
        institusi="UNKNOWN",
        program_studi=None,
        jenjang=None,
        tanggal_lulus=None
    )
    try:
        record = IjazahRecord(
            nomor_ijazah=nomor_ijazah,
            biodata=biodata,
            akademik=akademik,
            raw_ocr_confidence=avg_confidence
        )
        output = record.model_dump()
        if is_transcript:
            output["transcript_data"] = {
                "ipk": extract_ipk(ocr_text),
                "grades": extract_transcript_rows(ocr_text)
            }
        return output
    except ValidationError as e:
        return {
            "status": "error",
            "message": "Validation failed on extracted data",
            "details": e.errors(),
            "raw_text": ocr_text
        }

def process_file(file_path: str, is_transcript: bool = False) -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found on {file_path}")
    ext = file_path.lower().split('.')[-1]
    if ext in ['png', 'jpg', 'jpeg']:
        return [process_single_image(file_path, is_transcript)]
    elif ext == 'pdf':
        results = []
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(file_path, output_folder=path, fmt='png')
            for image_file in glob.glob(os.path.join(path, "*.png")):
                results.append(process_single_image(image_file, is_transcript))
        return results
    else:
        raise ValueError(f"Unsupported format: {ext}")

def process_directory(folder_path: str, is_transcript: bool = False) -> Dict[str, List[Dict[str, Any]]]:
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Directory not found: {file_path}")
    supported_extensions = ('*.png', '*.jpg', '*.jpeg', '*.pdf')
    files_to_process = []
    for ext in supported_extensions:
        files_to_process.extend(glob.glob(os.path.join(folder_path, ext)))
        files_to_process.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    results = {}
    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        print(f"Processing {filename}")
        try:
            parsed_data = process_file(file_path, is_transcript)
            results[filename] = parsed_data
        except Exception as e:
            results[filename] = [{
                "status": "error",
                "message": f"Pipeline crashed: {str(e)}"
            }]
    return results
