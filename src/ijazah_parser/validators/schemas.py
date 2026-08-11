from datetime import date
from typing import Optional
from pydantic import Basemodel, Field, field_validator
from ijazah_parser.validators.sivil import validate_sivil_year

class BiodataSchema(BaseModel):
    nama: str = Field(..., description="Full name")
    tempat_lahir: Optional[str] = Field(None, description="Birthplace")
    tanggal_lahir: Optional[str] = Field(None, description="Birthdate")
    nomor_induk: Optional[str] = Field(None, description="NIM")

class AcademicScheme(BaseModel):
    institusi: str = Field(..., description="College's full name")
    program_studi: Optional[str] = Field(None, description="Major/Study Program")
    jenjang: Optional[str] = Field(None, description="Degree Level")
    tanggal_lulus: Optional[str] = Field(None, description="Graduation Date")

class IjazahRecord(BaseModel):
    nomor_ijazah: Optional[str] = Field(None, description="Serial Number")
    biodata: BiodataSchema
    akademik: AcademicScheme
    raw_ocr_confidence: float = Field(0.0, ge=0.0, le=1.0, description="Average OCR Confidence Score")
    @field_validator("nomor_ijazah")
    @classmethod
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        if value:
            return value.strip().upper()
        return value