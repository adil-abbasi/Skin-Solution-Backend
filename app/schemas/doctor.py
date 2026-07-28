from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, field_serializer


class DoctorBase(BaseModel):

    name: str

    specialization: str

    department: str

    consultation_fee: float = 1000


    phone: str | None = None

    email: str | None = None

    room_no: str | None = None


    available_days: str = (
        "Monday,Tuesday,Wednesday,Thursday,Friday"
    )


    start_time: str | None = None

    end_time: str | None = None



class DoctorCreate(DoctorBase):
    pass



class DoctorUpdate(BaseModel):

    name: str | None = None

    specialization: str | None = None

    department: str | None = None


    consultation_fee: float | None = None


    phone: str | None = None

    email: str | None = None

    room_no: str | None = None


    available_days: str | None = None


    start_time: str | None = None

    end_time: str | None = None


    is_active: bool | None = None



class DoctorResponse(BaseModel):

    id: int

    doctor_code: str


    name: str

    specialization: str

    department: str


    consultation_fee: float


    phone: str | None = None

    email: str | None = None

    room_no: str | None = None


    available_days: str


    start_time: time | None = None

    end_time: time | None = None


    is_active: bool


    created_at: datetime

    updated_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )


    @field_serializer(
        "start_time",
        "end_time"
    )
    def serialize_time(
        self,
        value: time | None
    ):

        if value:
            return value.strftime("%H:%M")

        return None