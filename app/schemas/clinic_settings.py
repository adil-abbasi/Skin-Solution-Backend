from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class ClinicSettings(Base):

    __tablename__ = "clinic_settings"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    clinic_name: Mapped[str] = mapped_column(
        String(100),
        default="My Clinic"
    )


    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )


    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )


    footer_text: Mapped[str] = mapped_column(
        String(255),
        default="Thank you for visiting"
    )


    show_doctor: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


    show_patient: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


    currency: Mapped[str] = mapped_column(
        String(10),
        default="Rs."
    )


    default_fee: Mapped[int] = mapped_column(
        Integer,
        default=1000
    )


    auto_reset_token: Mapped[bool] = mapped_column(
        Boolean,
        default=True
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