from datetime import datetime, date, time
from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    String,
    Date,
    Time,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base

if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.doctor import Doctor


class OPDVisit(Base):
    __tablename__ = "opd_visits"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id"),
        nullable=False,
    )

    token_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    visit_date: Mapped[date] = mapped_column(
        Date,
        default=date.today,
    )

    visit_day: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    visit_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    consultation_fee: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    visit_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    discount: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    amount_received: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    payment_method: Mapped[str] = mapped_column(
        String(20),
        default="Cash",
    )

    payment_status: Mapped[str] = mapped_column(
        String(20),
        default="Paid",
    )

    print_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Waiting",
    )

    cancel_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="visits",
    )

    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="visits",
    )