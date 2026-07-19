from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)

from app.services.appointment_service import (
    AppointmentService
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post(
    "/",
    response_model=AppointmentResponse
)
def create(
    data: AppointmentCreate,
    db: Session = Depends(get_db)
):

    return AppointmentService.create(
        db,
        data
    )


@router.get(
    "/",
    response_model=list[AppointmentResponse]
)
def get_all(
    db: Session = Depends(get_db)
):

    return AppointmentService.get_all(db)


@router.get(
    "/today",
    response_model=list[AppointmentResponse]
)
def today(
    db: Session = Depends(get_db)
):

    return AppointmentService.today(db)


@router.get(
    "/upcoming",
    response_model=list[AppointmentResponse]
)
def upcoming(
    db: Session = Depends(get_db)
):

    return AppointmentService.upcoming(db)


@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def update(
    appointment_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db)
):

    appointment = AppointmentService.update(
        db,
        appointment_id,
        data
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


@router.put(
    "/{appointment_id}/cancel",
    response_model=AppointmentResponse
)
def cancel(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = AppointmentService.cancel(
        db,
        appointment_id
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment