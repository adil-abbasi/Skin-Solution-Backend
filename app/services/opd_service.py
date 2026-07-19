from sqlalchemy.orm import Session

from app.models.opd_visit import OPDVisit
from app.models.patient import Patient
from app.models.doctor import Doctor
from datetime import date

class OPDService:


    @staticmethod
    def today_queue(db: Session):

        visits = (
            db.query(OPDVisit)
            .filter(
                OPDVisit.visit_date == date.today()
            )
            .order_by(OPDVisit.token_number)
            .all()
        )

        result = []

        for visit in visits:

            result.append({
                "visit_id": visit.id,
                "token_number": visit.token_number,

                "patient_code": visit.patient.patient_code,
                "patient_name": visit.patient.name,
                "phone": visit.patient.phone,

                "doctor_name": visit.doctor.name,

                "visit_date": visit.visit_date,
                "visit_time": visit.visit_time,

                "consultation_fee": visit.consultation_fee,

                "status": visit.status
            })

        return result
    @staticmethod
    def complete_visit(db: Session, visit_id: int):

        visit = db.query(OPDVisit).filter(
            OPDVisit.id == visit_id
        ).first()

        if not visit:
            return False

        visit.status = "Completed"

        db.commit()

        return True
    
@staticmethod
def cancel_visit(
    db: Session,
    visit_id: int,
    reason: str
):

    visit = db.query(OPDVisit).filter(
        OPDVisit.id == visit_id
    ).first()

    if not visit:
        return False

    visit.status = "Cancelled"
    visit.cancel_reason = reason

    db.commit()

    return True
        
    @staticmethod
    def get_token_slip(
        db: Session,
        visit_id: int
    ):

        visit = db.query(OPDVisit).filter(
            OPDVisit.id == visit_id
        ).first()


        if not visit:
            return None


        patient = db.query(Patient).filter(
            Patient.id == visit.patient_id
        ).first()


        doctor = db.query(Doctor).filter(
            Doctor.id == visit.doctor_id
        ).first()



        return {

            "token_number": visit.token_number,

            "patient_name": patient.name,
            "father_husband_name": patient.father_name,
            "age": patient.age,
            "gender": patient.gender,
            "phone": patient.phone,
            "patient_code": patient.patient_code,


            "doctor_name": doctor.name,
            "department": doctor.department,


            "visit_date": visit.visit_date,
            "visit_day": visit.visit_day,
            "visit_time": visit.visit_time,


            "consultation_fee": visit.consultation_fee,

            "status": visit.status
        }