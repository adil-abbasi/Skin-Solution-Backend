from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OPDVisitCreate(BaseModel):
    patient_id: int
    doctor_id: int


class OPDVisitResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int

    token_number: int

    visit_date: date
    visit_day: str
    visit_time: time

    consultation_fee: float

    status: str

    cancel_reason: Optional[str] = None

    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )