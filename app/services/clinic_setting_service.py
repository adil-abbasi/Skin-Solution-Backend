from sqlalchemy.orm import Session

from app.models.clinic_setting import ClinicSetting
from app.schemas.clinic_setting import (
    ClinicSettingCreate,
    ClinicSettingUpdate,
)


class ClinicSettingService:

    @staticmethod
    def get(db: Session):

        setting = db.query(ClinicSetting).first()

        if not setting:

            setting = ClinicSetting(
                clinic_name="My Clinic",
                clinic_address="Clinic Address",
                clinic_phone="0000-0000000",
                clinic_email="clinic@example.com",
                receipt_footer="Thank you for visiting.",
                logo_path=""
            )

            db.add(setting)
            db.commit()
            db.refresh(setting)

        return setting

    @staticmethod
    def update(
        db: Session,
        data: ClinicSettingUpdate
    ):

        setting = db.query(ClinicSetting).first()

        if not setting:

            setting = ClinicSetting(
                clinic_name=data.clinic_name or "My Clinic",
                clinic_address=data.clinic_address or "Clinic Address",
                clinic_phone=data.clinic_phone or "0000-0000000",
                clinic_email=data.clinic_email,
                receipt_footer=data.receipt_footer,
                logo_path=data.logo_path,
            )

            db.add(setting)

        else:

            update_data = data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(setting, key, value)

        db.commit()
        db.refresh(setting)

        return setting