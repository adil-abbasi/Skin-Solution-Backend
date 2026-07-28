from datetime import date, time
from typing import List

from pydantic import BaseModel


class OPDHistoryRecord(BaseModel):
    id: int
    token_number: int
    visit_number: str

    patient_name: str
    doctor_name: str

    visit_date: date
    visit_time: time

    consultation_fee: float
    discount: float
    amount_received: float

    payment_method: str
    status: str

    class Config:
        from_attributes = True


class OPDHistorySummary(BaseModel):
    total_patients: int
    waiting: int
    completed: int
    cancelled: int
    total_revenue: float


class Pagination(BaseModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int


class OPDHistoryResponse(BaseModel):
    summary: OPDHistorySummary
    pagination: Pagination
    records: List[OPDHistoryRecord]