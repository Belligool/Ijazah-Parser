import re
from typing import Dict, List

OCR_NUMERIC_CORRECTIONS: Dict[str, str] = {
    "O": "0", "o": "0", "Q": "0", "D": "0",
    "I": "1", "l": "1", "i": "1", "|": "1",
    "Z": "2", "z": "2",
    "S": "5", "s": "5",
    "G": "6", "b": "6",
    "B": "8",
    "g": "9",
}

INDONESIAN_MONTHS: Dict[str, str] = {
    "januari": "01", "jan": "01",
    "februari": "02", "feb": "02", "pebruari": "02",
    "maret": "03", "mar": "03",
    "april": "04", "apr": "04",
    "mei": "05", "may": "05",
    "juni": "06", "jun": "06",
    "juli": "07", "jul": "07",
    "agustus": "08", "agu": "08", "ags": "08",
    "september": "09", "sep": "09", "sept": "09",
    "oktober": "10", "okt": "10",
    "november": "11", "nov": "11", "nopember": "11",
    "desember": "12", "des": "12",
}

# Regexx
REGEX_TANGGAL_ID = re.compile(
    r"\b(\d{1,2})\s+(Januari|Februari|Pebruari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Nopember|Desember)\s+(\d{4})\b",
    re.IGNORECASE,
)

REGEX_PIN_SIVIL = re.compile(
    r"(?:\b(?:No\.\s*Ijazah|PIN|Nomor\s*Ijazah|No\.\s*Seri)\s*[:;\-\.]?\s*)?(\b[\dOoQDIli\|ZzSsGbB]{14,15}\b)",
    re.IGNORECASE,
)

REGEX_IJAZAH_SEKOLAH = re.compile(
    r"\b((?:DN|LN|DP)-\d{2}\s*\/\s*(?:D|M|P)-(?:SD|SMP|SMA|SMK|SLB)\s*\/\s*(?:K13|13|06|KM|\d{2})\s*\/\s*(?:\d{2}\/)?\d{7})\b",
    re.IGNORECASE,
)

REGEX_NISN = re.compile(
    r"(?:\bNISN\s*[:;\-\.]?\s*)?(\b[\dOoQDIli\|ZzSsGbB]{10}\b)",
    re.IGNORECASE,
)

REGEX_IPK = re.compile(
    r"(?:IPK|Indeks\s*Prestasi\s*Kumulatif)\s*[:;\-\=]?\s*([0-4][\.\,]\d{1,2})",
    re.IGNORECASE
)

REGEX_TRANSCRIPT_ROW = re.compile(
    r"^\s*(?:\d{1,3}[\.\)]?\s+)?([A-Za-z0-9\s\-\&\,]+?)\s+([1-6])\s+([A-E][B-D]?)\b",
    re.MULTILINE | re.IGNORECASE
)

LABEL_NAMA = re.compile(
    r"(?:Nama\s*(?:Mahasiswa|Siswa)?|menyatakan\s*bahwa|memberikan\s*(?:ijazah\s*)?kepada)\s*[:;\-]?\s*[\d\s\.\,]*([A-Z][A-Za-z\s\.,'`]+?)(?=\s+lahir\b|\s+diterima\b|\s+NIM\b|\s+NISN\b|\s+di\b|$)", 
    re.IGNORECASE
)

LABEL_TEMPAT_TANGGAL_LAHIR = re.compile(
    r"(?:Tempat,\s*tanggal\s*lahir\s*[:;\-]?|lahir\s*di)\s*([A-Za-z\s]+)(?:,|\s*tanggal)\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})", 
    re.IGNORECASE
)
LABEL_NOMOR_INDUK = re.compile(
    r"(?:Nomor\s*Induk\s*(?:Mahasiswa|Siswa)?|NIM|NISN)\s*[:;\-]?\s*([A-Z0-9][\w\s\-]+)", 
    re.IGNORECASE
)