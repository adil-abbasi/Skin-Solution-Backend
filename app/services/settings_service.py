from sqlalchemy.orm import Session

from app.models.settings import Setting
from app.schemas.settings import SettingsUpdate


class SettingsService:

    @staticmethod
    def get_settings(db: Session):

        settings = db.query(Setting).first()

        if not settings:

            settings = Setting()

            db.add(settings)
            db.commit()
            db.refresh(settings)

        return settings

    @staticmethod
    def update_settings(
        db: Session,
        data: SettingsUpdate
    ):

        settings = db.query(Setting).first()

        if not settings:

            settings = Setting()

            db.add(settings)
            db.commit()
            db.refresh(settings)

        for key, value in data.model_dump().items():
            setattr(settings, key, value)

        db.commit()
        db.refresh(settings)

        return settings