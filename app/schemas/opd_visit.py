from datetime import date, time, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from datetime import date, time
from pydantic import BaseModel, ConfigDict
# ==========================================================
# Create Visit
# ==========================================================

class OPDVisitCreate(BaseModel):

    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)

    consultation_fee: float = Field(..., ge=0)
    discount: float = Field(default=0, ge=0)
    amount_received: float = Field(..., ge=0)

    payment_method: Literal[
        "Cash",
        "Card",
        "JazzCash",
        "EasyPaisa"
    ] = "Cash"


# ==========================================================
# Update Visit
# ==========================================================

class OPDVisitUpdate(BaseModel):

    consultation_fee: float | None = None
    discount: float | None = None
    amount_received: float | None = None

    payment_method: str | None = None
    payment_status: str | None = None

    status: str | None = None
    cancel_reason: str | None = None


# ==========================================================
# Visit Response
# ==========================================================

class OPDVisitResponse(BaseModel):

    id: int

    visit_number: str

    patient_id: int
    doctor_id: int

    token_number: int

    visit_date: date
    visit_day: str
    visit_time: time

    consultation_fee: float
    discount: float
    amount_received: float

    payment_method: str
    payment_status: str

    print_count: int

    status: str
    cancel_reason: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# Professional Token Response
# ==========================================================

class TokenPrintResponse(BaseModel):
    clinic_name: str

    visit_number: str
    token_number: int

    patient_name: str
    father_name: str | None = None

    gender: str
    age: int

    doctor_name: str

    consultation_fee: float
    payment_method: str

    visit_date: date
    visit_time: time

    model_config = ConfigDict(from_attributes=True)