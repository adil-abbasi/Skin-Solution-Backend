from datetime import date, datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.opd_visit import OPDVisit

from app.schemas.opd_visit import (
    OPDVisitCreate,
    OPDVisitUpdate,
)

class OPDService:


    # ==========================================================
    # Generate Visit Number
    # ==========================================================

    @staticmethod
    def generate_visit_number(db: Session):

        today = date.today().strftime("%Y%m%d")

        count = (
            db.query(OPDVisit)
            .filter(
                OPDVisit.visit_date == date.today()
            )
            .count()
        )

        return f"VIS-{today}-{count + 1:06d}"



    # ==========================================================
    # Generate Token
    # ==========================================================

    @staticmethod
    def generate_token(db: Session):

        last_token = (
            db.query(
                func.max(OPDVisit.token_number)
            )
            .filter(
                OPDVisit.visit_date == date.today()
            )
            .scalar()
        )


        if last_token is None:
            return 1


        return last_token + 1



    # ==========================================================
    # Get Patient
    # ==========================================================

    @staticmethod
    def get_patient(
        db: Session,
        patient_id:int
    ):

        patient = (
            db.query(Patient)
            .filter(
                Patient.id == patient_id,
                Patient.is_active == True
            )
            .first()
        )


        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )


        return patient



    # ==========================================================
    # Get Doctor
    # ==========================================================

    @staticmethod
    def get_doctor(
        db:Session,
        doctor_id:int
    ):

        doctor = (
            db.query(Doctor)
            .filter(
                Doctor.id == doctor_id,
                Doctor.is_active == True
            )
            .first()
        )


        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )


        return doctor



    # ==========================================================
    # Get Visit
    # ==========================================================

    @staticmethod
    def get_visit(
        db:Session,
        visit_id:int
    ):

        visit = (
            db.query(OPDVisit)
            .options(
                joinedload(OPDVisit.patient),
                joinedload(OPDVisit.doctor)
            )
            .filter(
                OPDVisit.id == visit_id
            )
            .first()
        )


        if not visit:

            raise HTTPException(
                status_code=404,
                detail="Visit not found"
            )


        return visit



    # ==========================================================
    # Create Visit
    # ==========================================================

    @staticmethod
    def create_visit(
        db:Session,
        visit:OPDVisitCreate
    ):


        patient = OPDService.get_patient(
            db,
            visit.patient_id
        )


        doctor = OPDService.get_doctor(
            db,
            visit.doctor_id
        )


        token = OPDService.generate_token(db)


        visit_number = OPDService.generate_visit_number(db)



        db_visit = OPDVisit(

            visit_number=visit_number,

            patient_id=patient.id,

            doctor_id=doctor.id,

            token_number=token,

            visit_date=date.today(),

            visit_day=date.today().strftime("%A"),

            visit_time=datetime.now().time(),

            consultation_fee=visit.consultation_fee,

            discount=visit.discount,

            amount_received=visit.amount_received,

            payment_method=visit.payment_method,

            payment_status="Paid",

            print_count=0,

            status="Waiting"

        )


        db.add(db_visit)

        db.commit()

        db.refresh(db_visit)


        return db_visit



    # ==========================================================
    # All Visits
    # ==========================================================

    @staticmethod
    def get_all(db:Session):

        return (

            db.query(OPDVisit)

            .options(
                joinedload(OPDVisit.patient),
                joinedload(OPDVisit.doctor)
            )

            .order_by(
                OPDVisit.created_at.desc()
            )

            .all()

        )



    # ==========================================================
    # Today's Queue
    # ==========================================================

    @staticmethod
    def get_today_visits(db: Session):

      visits = (
        db.query(OPDVisit)
        .options(
            joinedload(OPDVisit.patient),
            joinedload(OPDVisit.doctor)
        )
        .filter(
            OPDVisit.visit_date == date.today()
        )
        .order_by(
            OPDVisit.token_number
        )
        .all()
    )

      return [
         {
            "id": visit.id,
            "visit_number": visit.visit_number,
            "patient_id": visit.patient_id,
            "doctor_id": visit.doctor_id,

            "patient_name": visit.patient.name,
            "father_name": visit.patient.father_name,
            "doctor_name": visit.doctor.name,

            "token_number": visit.token_number,

            "consultation_fee": visit.consultation_fee,
            "discount": visit.discount,
            "amount_received": visit.amount_received,

            "payment_method": visit.payment_method,
            "payment_status": visit.payment_status,

            "status": visit.status,
            "cancel_reason": visit.cancel_reason,

            "visit_date": visit.visit_date,
            "visit_day": visit.visit_day,
            "visit_time": visit.visit_time,

            "print_count": visit.print_count,
            "created_at": visit.created_at,
            "updated_at": visit.updated_at,
        }
        for visit in visits
    ]


    # ==========================================================
    # Update Visit
    # ==========================================================

    @staticmethod
    def update_visit(
        db:Session,
        visit_id:int,
        visit:OPDVisitUpdate
    ):

        db_visit = OPDService.get_visit(
            db,
            visit_id
        )


        data = visit.model_dump(
            exclude_unset=True
        )


        for key,value in data.items():

            setattr(
                db_visit,
                key,
                value
            )


        db.commit()

        db.refresh(db_visit)


        return db_visit



    # ==========================================================
    # Change Status
    # ==========================================================

    @staticmethod
    def change_status(
        db:Session,
        visit_id:int,
        status:str
    ):


        visit = OPDService.get_visit(
            db,
            visit_id
        )


        allowed=[
            "Waiting",
            "Called",
            "Completed",
            "Cancelled"
        ]


        if status not in allowed:

            raise HTTPException(
                status_code=400,
                detail="Invalid status"
            )


        visit.status=status


        db.commit()

        db.refresh(visit)


        return visit



    # ==========================================================
    # Cancel Visit
    # ==========================================================

    @staticmethod
    def cancel_visit(
        db:Session,
        visit_id:int,
        reason:str
    ):

        visit = OPDService.get_visit(
            db,
            visit_id
        )


        visit.status="Cancelled"

        visit.cancel_reason=reason


        db.commit()

        db.refresh(visit)


        return visit



    # ==========================================================
    # Reprint
    # ==========================================================

    @staticmethod
    def reprint_token(
        db:Session,
        visit_id:int
    ):


        visit = OPDService.get_visit(
            db,
            visit_id
        )


        visit.print_count += 1


        db.commit()


        return OPDService.get_print_data(
            db,
            visit_id
        )



    # ==========================================================
    # Print Data
    # ==========================================================

    @staticmethod
    def get_print_data(
        db: Session,
        visit_id: int
    ):
        visit = (
            db.query(OPDVisit)
            .options(
                joinedload(OPDVisit.patient),
                joinedload(OPDVisit.doctor)
            )
            .filter(OPDVisit.id == visit_id)
            .first()
        )

        if not visit:
            raise HTTPException(
                status_code=404,
                detail="Visit not found"
            )

        return {
            "clinic_name": "SkinSolutions",
            "visit_number": visit.visit_number,
            "token_number": visit.token_number,

            "patient_name": visit.patient.name,
            "father_name": visit.patient.father_name,
            "age": visit.patient.age,
            "gender": visit.patient.gender,

            "doctor_name": visit.doctor.name,

            "consultation_fee": visit.consultation_fee,
            "payment_method": visit.payment_method,

            "visit_date": visit.visit_date,
            "visit_day": visit.visit_day,
            "visit_time": visit.visit_time,
        }