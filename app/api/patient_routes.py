from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
)

from app.services.patient_service import PatientService


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# ==========================================================
# Create Patient
# ==========================================================

@router.post(
    "/",
    response_model=PatientResponse
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return PatientService.create(
        db,
        patient
    )



# ==========================================================
# Search Patients
# ==========================================================

@router.get(
    "/search",
    response_model=list[PatientResponse]
)
def search_patients(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return PatientService.search(
        db,
        q
    )



# ==========================================================
# Get All Patients
# ==========================================================

@router.get(
    "/",
    response_model=list[PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return PatientService.get_all(
        db
    )



# ==========================================================
# Get Single Patient
# ==========================================================

@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    patient = PatientService.get(
        db,
        patient_id
    )


    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    return patient



# ==========================================================
# Update Patient
# ==========================================================

@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    updated = PatientService.update(
        db,
        patient_id,
        patient
    )


    if not updated:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    return updated



# ==========================================================
# Patient Visit History
# ==========================================================

@router.get(
    "/{patient_id}/visits"
)
def patient_visits(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return PatientService.get_patient_visits(
        db,
        patient_id
    )



# ==========================================================
# Delete Patient (Soft Delete)
# ==========================================================

@router.delete(
    "/{patient_id}"
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    deleted = PatientService.delete(
        db,
        patient_id
    )


    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    return {
        "message": "Patient deactivated successfully"
    }