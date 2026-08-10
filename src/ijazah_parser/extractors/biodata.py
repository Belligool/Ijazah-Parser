import re
from typing import Optional, Tuple
from ijazah_parser.config import *
from ijazah_parser.validator.schemas import *

def clean_name_string(name_str: str) -> str:
    cleaned = re.sub(r'[^A-Za-z\s\.,\']', '', name_str)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned.title()

def normalize_indonesian_date(raw_date_str: str) -> Optional[str]:
    match = REGEX_TANGGAL_ID.search(raw_date_str)
    if not match:
        return raw_date_str.strip()
    day, month_str, year = match.groups()
    day = day.zfill(2)
    month_key = month_str.strip().lower()
    month = INDONESIAN_MONTHS.get(month_key, "01")
    return f"{year}-{month}-{day}"

def extract_biodata(ocr_text: str) -> BiodataSchema:
    nama_match = LABEL_NAMA.search(ocr_text)
    nama_val = clean_name_string(nama_match.group(1)) if nama_match else "UNKNOWN"
    tempat_lahir_val = None
    tanggal_lahir_val = None
    ttl_match = LABEL_TEMPAT_TANGGAL_LAHIR.search(ocr_text)
    if ttl_match:
        tempat_lahir_val = ttl_match.group(1).strip().title()
        raw_date = ttl_match.group(2).strip()
        tanggal_lahir_val = normalize_indonesian_date(raw_date)
    else:
        date_match = REGEX_TANGGAL_ID.search(ocr_text)
        if date_match:
            tanggal_lahir_val = normalize_indonesian_date(date_match.group(0))
    # NIM/NISN
    nomor_induk_val = None
    induk_match = LABEL_NOMOR_INDUK.search(ocr_text)
    if induk_match:
        nomor_induk_val = re.sub(r'[^\w]', '', induk_match.group(1).strip())
    
    return BiodataSchema(
        nama=nama_val,
        tempat_lahir=tempat_lahir_val,
        tanggal_lahir=tanggal_lahir_val,
        nomor_induk=nomor_induk_val
    )
