from datetime import date, time

from pydantic import BaseModel


class AppointmentCreate(BaseModel):

    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    remarks: str | None = None


class AppointmentUpdate(BaseModel):

    appointment_date: date | None = None
    appointment_time: time | None = None
    status: str | None = None
    remarks: str | None = None


class AppointmentResponse(BaseModel):

    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str
    remarks: str | None

    class Config:
        from_attributes = True