from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class ClinicSetting(Base):

    __tablename__ = "clinic_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    clinic_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    clinic_address: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    clinic_phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    clinic_email: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    receipt_footer: Mapped[str] = mapped_column(
        String(300),
        nullable=True
    )

    logo_path: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )