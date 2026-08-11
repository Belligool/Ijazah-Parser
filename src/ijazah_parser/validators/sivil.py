import re
from typing import Dict, Optional

def parse_sivil_pin(pin: str) -> Optional[Dict[str, str]]:
    if not pin:
        return None
    cleaned_pin = re.sub(r'[^\d]', '', pin)
    return {
        "kode_prodi": cleaned_pin[0:5],
        "tahun_lulus": cleaned_pin[5:9],
        "nomor_urut": cleaned_pin[9:14],
        "check_digit": cleaned_pin[14:] if len(cleaned_pin) == 15 else None
    }

def validate_sivil_year(pin: str, tanggal_lulus: Optional[str]) -> bool:
    parsed = parse_sivil_pin(pin)
    if not parsed or not tanggal_lulus:
        return True
    pin_year = parsed["tahun_lulus"]
    grad_year = tanggal_lulus[:4]
    return pin_year == grad_year

def is_plausible_sivil_pin(pin: str) -> bool:
    parsed = parse_sivil_pin(pin)
    if not parsed:
        return False
    try:
        tahun = int(parsed["tahun_lulus"])
        if not (2000 <= tahun <= 2050):
            return False
    except ValueError:
        return False
    return True
