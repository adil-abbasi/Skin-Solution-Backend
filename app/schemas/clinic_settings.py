from pydantic import BaseModel, EmailStr
from typing import Optional


class ClinicSettingBase(BaseModel):
    clinic_name: str
    clinic_address: str
    clinic_phone: str
    clinic_email: Optional[EmailStr] = None
    receipt_footer: Optional[str] = None
    logo_path: Optional[str] = None


class ClinicSettingCreate(ClinicSettingBase):
    pass


class ClinicSettingUpdate(BaseModel):
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    clinic_phone: Optional[str] = None
    clinic_email: Optional[EmailStr] = None
    receipt_footer: Optional[str] = None
    logo_path: Optional[str] = None


class ClinicSettingResponse(ClinicSettingBase):
    id: int

    class Config:
        from_attributes = True