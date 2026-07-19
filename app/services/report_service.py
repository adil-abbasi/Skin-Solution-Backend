from sqlalchemy.orm import Session

from app.models.opd_visit import OPDVisit

class ReportService:

    @staticmethod
    def today(db: Session):

        return db.query(OPDVisit).all()