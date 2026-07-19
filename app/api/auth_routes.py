from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.user import UserLogin
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = UserLogin(
        username=form_data.username,
        password=form_data.password
    )

    result = AuthService.login(db, user)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    return result

@router.post("/change-password")
def change_password():

    return {
        "message": "Coming Soon"
    }


@router.get("/me")
def me():

    return {
        "message": "Coming Soon"
    }