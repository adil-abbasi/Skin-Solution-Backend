import io
import pandas as pd

from app.models.opd_visit import OPDVisit


class ExportService:


    @staticmethod
    def export_visits(
        db,
        start_date,
        end_date,
        filename
    ):

        visits = (
            db.query(OPDVisit)
            .filter(
                OPDVisit.visit_date.between(
                    start_date,
                    end_date
                )
            )
            .all()
        )


        rows = []

        for visit in visits:

            rows.append({

                "Token Number": visit.token_number,

                "Visit Number": visit.visit_number,

                "Patient":
                    visit.patient.name
                    if visit.patient
                    else "Unknown",

                "Doctor":
                    visit.doctor.name
                    if visit.doctor
                    else "Unknown",

                "Date": visit.visit_date,

                "Time": visit.visit_time,

                "Fee": visit.consultation_fee,

                "Discount": visit.discount,

                "Received": visit.amount_received,

                "Payment Method": visit.payment_method,

                "Status": visit.status,

            })


        df = pd.DataFrame(rows)

        df.to_csv(
            filename,
            index=False
        )



    @staticmethod
    def export_opd_history(
        db,
        period="today",
        search=None,
        doctor_id=None,
        status=None,
    ):

        visits = (
            db.query(OPDVisit)
            .all()
        )


        rows = []


        for visit in visits:


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


            if search:

                if search.lower() not in patient_name.lower():

                    continue


            if doctor_id:

                if visit.doctor_id != doctor_id:

                    continue


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


        dataframe = pd.DataFrame(rows)


        output = io.BytesIO()


        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            dataframe.to_excel(
                writer,
                index=False,
                sheet_name="OPD History"
            )


        output.seek(0)


        return output