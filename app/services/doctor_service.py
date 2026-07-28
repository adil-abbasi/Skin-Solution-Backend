from datetime import datetime
import io
import pandas as pd
from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.opd_visit import OPDVisit
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.utils.code_generator import generate_code


class DoctorService:

    @staticmethod
    def _convert_time(value):
        """
        Convert frontend time string to Python time object.
        Example:
        "12:30" -> datetime.time(12,30)
        """

        if not value:
            return None

        if hasattr(value, "hour"):
            return value

        return datetime.strptime(
            value,
            "%H:%M"
        ).time()


    @staticmethod
    def create_doctor(
        db: Session,
        doctor: DoctorCreate
    ):

        doctor_code = generate_code(
            db,
            Doctor,
            "DOC",
            "doctor_code"
        )

        data = doctor.model_dump()

        data["start_time"] = DoctorService._convert_time(
            data.get("start_time")
        )

        data["end_time"] = DoctorService._convert_time(
            data.get("end_time")
        )


        db_doctor = Doctor(
            doctor_code=doctor_code,
            **data
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

        db_doctor = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()


        if not db_doctor:
            return None


        data = doctor.model_dump(
            exclude_unset=True
        )


        if "start_time" in data:
            data["start_time"] = DoctorService._convert_time(
                data["start_time"]
            )


        if "end_time" in data:
            data["end_time"] = DoctorService._convert_time(
                data["end_time"]
            )


        for key, value in data.items():
            setattr(
                db_doctor,
                key,
                value
            )


        db.commit()
        db.refresh(db_doctor)

        return db_doctor



    @staticmethod
    def delete_doctor(
        db: Session,
        doctor_id: int
    ):

        db_doctor = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()


        if not db_doctor:
            return None


        db_doctor.is_active = False

        db.commit()
        db.refresh(db_doctor)

        return db_doctor



    @staticmethod
    def activate_doctor(
        db: Session,
        doctor_id: int
    ):

        db_doctor = db.query(Doctor).filter(
            Doctor.id == doctor_id
        ).first()


        if not db_doctor:
            return None


        db_doctor.is_active = True

        db.commit()
        db.refresh(db_doctor)

        return db_doctor



    @staticmethod
    def get_doctor_visits(
        db: Session,
        doctor_id: int
    ):

        return db.query(OPDVisit).filter(
            OPDVisit.doctor_id == doctor_id
        ).all()
    @staticmethod
    def export_opd_history(
        db,
        period="today",
        search=None,
        doctor_id=None,
        status=None,
    ):

        query = (
            db.query(OPDVisit)
            .all()
        )


        rows = []


        for visit in query:

            patient_name = (
                visit.patient.name
                if visit.patient
                else "Unknown"
            )


            doctor_name = (
                visit.doctor.name
                if visit.doctor
                else "Unknown"
            )


            # Search filter
            if search:

                if search.lower() not in patient_name.lower():

                    continue


            # Doctor filter
            if doctor_id:

                if visit.doctor_id != doctor_id:

                    continue


            # Status filter
            if status:

                if visit.status != status:

                    continue


            rows.append({

                "Token Number":
                    visit.token_number,

                "Visit Number":
                    visit.visit_number,

                "Patient Name":
                    patient_name,

                "Doctor Name":
                    doctor_name,

                "Visit Date":
                    visit.visit_date,

                "Visit Time":
                    visit.visit_time,

                "Consultation Fee":
                    visit.consultation_fee,

                "Discount":
                    visit.discount,

                "Amount Received":
                    visit.amount_received,

                "Payment Method":
                    visit.payment_method,

                "Payment Status":
                    visit.payment_status,

                "Status":
                    visit.status,

            })


        df = pd.DataFrame(rows)


        output = io.BytesIO()


        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="OPD History"
            )


        output.seek(0)


        return output