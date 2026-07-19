import csv
from datetime import date

from sqlalchemy.orm import Session

from app.models.opd_visit import OPDVisit


class ExportService:

    @staticmethod
    def export_visits(
        db: Session,
        start_date: date,
        end_date: date,
        filename: str
    ):

        visits = db.query(OPDVisit).filter(
            OPDVisit.visit_date >= start_date,
            OPDVisit.visit_date <= end_date
        ).all()

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Token",
                "Patient Code",
                "Patient",
                "Doctor",
                "Department",
                "Date",
                "Time",
                "Fee",
                "Status"
            ])

            for visit in visits:

                writer.writerow([
                    visit.token_number,
                    visit.patient.patient_code,
                    visit.patient.name,
                    visit.doctor.name,
                    visit.doctor.department,
                    visit.visit_date,
                    visit.visit_time,
                    visit.consultation_fee,
                    visit.status
                ])

        return filename