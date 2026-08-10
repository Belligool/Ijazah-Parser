import re
from typing import Optional
from ijazah_parser.config import *

def sanitize_numeric_ocr(text: str) -> str:
    cleaned = text.strip()
    for char, digit in OCR_NUMERIC_CORRECTIONS.items():
        cleaned = cleaned.replace(char, digit)
    return re.sub(r'[^\d]', '', cleaned)

def extract_pin_sivil(ocr_text: str) -> Optional[str]:
    match = REGEX_PIN_SIVIL.search(ocr_text)
    if match:
        raw_pin = match.group(1)
        return sanitize_numeric_ocr(raw_pin)
    return None

def extract_nisn(ocr_text: str) -> Optional[str]:
    match = REGEX_NISN.search(ocr_text)
    if match:
        raw_nisn = match.group(1)
        return sanitize_numeric_ocr(raw_nisn)
    return None

def extract_ijazah_sekolah(ocr_text: str) -> Optional[str]:
    match = REGEX_IJAZAH_SEKOLAH.search(ocr_text)
    if match:
        raw_serial = match.group(1)
        cleaned_serial = re.sub(r'\s+', '', raw_serial)
        return cleaned_serial.upper()
    return None

