from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.opd_visit import OPDVisit
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.utils.code_generator import generate_code


class PatientService:

    @staticmethod
    def create(db: Session, patient: PatientCreate):

        code = generate_code(
            db,
            Patient,
            "PAT",
            "patient_code"
        )

        db_patient = Patient(
            patient_code=code,
            **patient.model_dump()
        )

        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

        return db_patient

    @staticmethod
    def get_all(db: Session):
        return db.query(Patient).all()

    @staticmethod
    def get(db: Session, patient_id: int):
        return db.query(Patient).filter(
            Patient.id == patient_id
        ).first()

    @staticmethod
    def search(db: Session, query: str):

        return db.query(Patient).filter(
            Patient.is_active == True,
            or_(
                Patient.patient_code.ilike(f"%{query}%"),
                Patient.name.ilike(f"%{query}%"),
                Patient.phone.ilike(f"%{query}%"),
                Patient.cnic.ilike(f"%{query}%")
            )
        ).all()

    @staticmethod
    def update(
        db: Session,
        patient_id: int,
        patient: PatientUpdate
    ):

        obj = db.query(Patient).filter(
            Patient.id == patient_id
        ).first()

        if not obj:
            return None

        for key, value in patient.model_dump(
            exclude_unset=True
        ).items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)

        return obj

    @staticmethod
    def get_patient_visits(db, patient_id):

     return db.query(OPDVisit).filter(
        OPDVisit.patient_id == patient_id
    ).all()
    
    @staticmethod
    def delete(
        db: Session,
        patient_id: int
    ):

        obj = db.query(Patient).filter(
            Patient.id == patient_id
        ).first()

        if not obj:
            return None

        obj.is_active = False

        db.commit()

        return obj