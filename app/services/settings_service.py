from sqlalchemy.orm import Session

from app.models.clinic_settings import ClinicSettings



class SettingsService:


    @staticmethod
    def get_settings(
        db: Session
    ):

        settings = db.query(
            ClinicSettings
        ).first()


        if not settings:

            settings = ClinicSettings()

            db.add(settings)

            db.commit()

            db.refresh(settings)


        return settings



    @staticmethod
    def update_settings(
        db: Session,
        data
    ):


        settings = SettingsService.get_settings(db)


        update_data = data.model_dump(
            exclude_unset=True
        )


        for key,value in update_data.items():

            setattr(
                settings,
                key,
                value
            )


        db.commit()

        db.refresh(settings)


        return settings