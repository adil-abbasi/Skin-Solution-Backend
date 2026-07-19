from pydantic import BaseModel
from datetime import date, time


class TokenSlipResponse(BaseModel):
    token_number: int

    patient_name: str
    father_husband_name: str

    age: int
    gender: str
    phone: str

    patient_code: str

    doctor_name: str
    department: str

    visit_date: date
    visit_day: str
    visit_time: time

    consultation_fee: float

    status: str

    class Config:
        from_attributes = True


class TodayQueueResponse(BaseModel):
    visit_id: int
    token_number: int

    patient_code: str
    patient_name: str
    phone: str

    doctor_name: str

    visit_date: date
    visit_time: time

    consultation_fee: float

    status: str

    class Config:
        from_attributes = True