from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    clinic_name: Mapped[str] = mapped_column(
        String(150),
        default="My Clinic"
    )

    address: Mapped[str] = mapped_column(
        String(255),
        default=""
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        default=""
    )

    email: Mapped[str] = mapped_column(
        String(120),
        default=""
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="PKR"
    )

    receipt_footer: Mapped[str] = mapped_column(
        String(255),
        default="Thank you for visiting."
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