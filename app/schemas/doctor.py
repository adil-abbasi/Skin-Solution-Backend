from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    doctor_code: str
    name: str
    specialization: str
    department: str
    consultation_fee: float
    phone: Optional[str] = None
    email: Optional[str] = None


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    department: str
    consultation_fee: float
    phone: str | None = None
    email: str | None = None


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    department: Optional[str] = None
    consultation_fee: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class DoctorResponse(DoctorBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)