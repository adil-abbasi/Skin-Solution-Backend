from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.dependencies.auth import admin_required

from app.schemas.backup import (
    BackupResponse,
    RestoreRequest,
    MessageResponse
)

from app.services.backup_service import BackupService


router = APIRouter(
    prefix="/backup",
    tags=["Backup"]
)


@router.post(
    "/create",
    response_model=BackupResponse
)
def create_backup(
    user=Depends(admin_required)
):

    filename = BackupService.backup()

    return {
        "message": "Backup created successfully",
        "filename": filename
    }


@router.get("/list")
def list_backups(
    user=Depends(admin_required)
):

    return BackupService.list_backups()


@router.post(
    "/restore",
    response_model=MessageResponse
)
def restore_backup(
    data: RestoreRequest,
    user=Depends(admin_required)
):

    backup_path = Path("backups") / data.filename

    ok = BackupService.restore(
        str(backup_path)
    )

    if not ok:

        raise HTTPException(
            status_code=404,
            detail="Backup file not found"
        )

    return {
        "message": "Database restored successfully"
    }


@router.get("/download/{filename}")
def download_backup(
    filename: str,
    user=Depends(admin_required)
):

    file = Path("backups") / filename

    if not file.exists():

        raise HTTPException(
            status_code=404,
            detail="Backup not found"
        )

    return FileResponse(
        path=str(file),
        media_type="application/octet-stream",
        filename=filename
    )