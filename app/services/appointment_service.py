from datetime import date

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate
)


class AppointmentService:

    @staticmethod
    def create(
        db: Session,
        data: AppointmentCreate
    ):

        appointment = Appointment(
            **data.model_dump()
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        return appointment

    @staticmethod
    def get_all(db: Session):

        return db.query(Appointment).order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        ).all()

    @staticmethod
    def today(db: Session):

        return db.query(Appointment).filter(
            Appointment.appointment_date == date.today()
        ).order_by(
            Appointment.appointment_time
        ).all()

    @staticmethod
    def upcoming(db: Session):

        return db.query(Appointment).filter(
            Appointment.appointment_date >= date.today()
        ).order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        ).all()

    @staticmethod
    def update(
        db: Session,
        appointment_id: int,
        data: AppointmentUpdate
    ):

        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()

        if not appointment:
            return None

        for key, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                appointment,
                key,
                value
            )

        db.commit()
        db.refresh(appointment)

        return appointment

    @staticmethod
    def cancel(
        db: Session,
        appointment_id: int
    ):

        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()

        if not appointment:
            return None

        appointment.status = "Cancelled"

        db.commit()

        return appointment