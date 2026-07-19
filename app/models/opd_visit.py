from datetime import datetime, date, time

from sqlalchemy import (
    Integer,
    String,
    Date,
    Time,
    DateTime,
    Float,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class OPDVisit(Base):

    __tablename__ = "opd_visits"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )


    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id"),
        nullable=False
    )


    token_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    visit_date: Mapped[date] = mapped_column(
        Date,
        default=date.today
    )


    visit_day: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )


    visit_time: Mapped[time] = mapped_column(
        Time,
        default=datetime.now().time
    )


    consultation_fee: Mapped[float] = mapped_column(
        Float,
        default=0
    )


    status: Mapped[str] = mapped_column(
        String(20),
        default="Waiting"
    )


    cancel_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    patient = relationship(
        "Patient"
    )


    doctor = relationship(
        "Doctor"
    )