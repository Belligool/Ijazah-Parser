from datetime import date
from typing import Optional
from pydantic import Basemodel, Field, field_validator

class BiodataSchema(BaseModel):
    nama: str = Field(..., description="Full name")
    tempat_lahir: Optional[str] = field(None, description="Birthplace")
    tanggal_lahir: Optional[str] = field(None, description="Birthdate")
    nomor_induk: Optional[str] = field(None, description="NIM")

class AcademicScheme(BaseModel):
    institusi: str = Field(..., description="College's full name")