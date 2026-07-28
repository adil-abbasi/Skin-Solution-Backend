from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database.database import Base


class ClinicSettings(Base):

    __tablename__ = "clinic_settings"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # Clinic Profile

    clinic_name = Column(
        String,
        default="My Clinic"
    )

    address = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    email = Column(
        String,
        nullable=True
    )


    logo = Column(
        String,
        nullable=True
    )


    footer_text = Column(
        String,
        nullable=True
    )



    # Print Settings

    show_doctor = Column(
        Boolean,
        default=True
    )


    show_patient = Column(
        Boolean,
        default=True
    )



    # OPD Settings

    auto_reset_token = Column(
        Boolean,
        default=True
    )


    opd_closing_time = Column(
        String,
        default="22:00"
    )


    token_prefix = Column(
        String,
        default="T"
    )



    # System

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )