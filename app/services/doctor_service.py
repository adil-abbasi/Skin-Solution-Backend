from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.utils.code_generator import generate_code


class DoctorService:


    @staticmethod
    def create_doctor(
        db: Session,
        doctor: DoctorCreate
    ):

        code = generate_code(
            db,
            Doctor,
            "DOC",
            "doctor_code"
        )


        db_doctor = Doctor(
            doctor_code=code,
            **doctor.model_dump()
        )


        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)

        return db_doctor



    @staticmethod
    def get_all_doctors(
        db: Session
    ):

        return db.query(Doctor).all()



    @staticmethod
    def get_doctor(
        db: Session,
        doctor_id: int
    ):

        return db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()



    @staticmethod
    def update_doctor(
        db: Session,
        doctor_id: int,
        doctor: DoctorUpdate
    ):

        obj = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()


        if not obj:
            return None


        for key,value in doctor.model_dump(
            exclude_unset=True
        ).items():

            setattr(obj,key,value)


        db.commit()
        db.refresh(obj)

        return obj



    @staticmethod
    def delete_doctor(
        db: Session,
        doctor_id:int
    ):

        obj = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()


        if not obj:
            return None


        obj.is_active = False

        db.commit()

        return obj