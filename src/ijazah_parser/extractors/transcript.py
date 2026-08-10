import re
from typing import List, Dict, Optional
from ijazah_parser.config import *

def extract_ipk(ocr_text: str) -> Optional[float]:
    match = REGEX_IPK.search(ocr_text)
    if match:
        raw_ipk = match.group(1).replace(",", ".")
        try:
            ipk_val = float(raw_ipk)
            if 0.0 <= ipk_val <= 4.0:
                return ipk_val
        except ValueError:
            return None
    return None

def clean_course_name(name_str: str) -> str:
    cleaned = re.sub(r'[^A-Za-z0-9\s\-\&]', '', name_str)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().title()

def extract_transcript_rows(ocr_text: str) -> List[Dict[str, str]]:
    rows = []
    for match in REGEX_TRANSCRIPT_ROW.finditer(ocr_text):
        raw_course = match.group(1)
        sks_str = match.group(2)
        grade = match.group(3).upper()
        cleaned_course = clean_course_name(raw_course)
        if cleaned_course.lower() in ["mata kuliah", "mata pelajaran", "course name"]:
            continue
        rows.append({
            "mata_kuliah": cleaned_course,
            "sks": int(sks_str),
            "nilai_huruf": grade
        })
    return rows