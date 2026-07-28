from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from app.services.user_service import UserService

from app.dependencies.auth import admin_required



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()





@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db:Session=Depends(get_db),
    user=Depends(admin_required)
):

    return UserService.get_all(db)





@router.post(
    "/",
    response_model=UserResponse
)
def create_user(
    data:UserCreate,
    db:Session=Depends(get_db),
    user=Depends(admin_required)
):

    result = UserService.create(
        db,
        data
    )


    if not result:
        raise HTTPException(
            400,
            "Username already exists"
        )


    return result






@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id:int,
    data:UserUpdate,
    db:Session=Depends(get_db),
    user=Depends(admin_required)
):

    result = UserService.update(
        db,
        user_id,
        data
    )


    if not result:
        raise HTTPException(
            404,
            "User not found"
        )


    return result






@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id:int,
    db:Session=Depends(get_db),
    user=Depends(admin_required)
):

    result = UserService.delete(
        db,
        user_id
    )


    if not result:
        raise HTTPException(
            404,
            "User not found"
        )


    return {
        "message":"User disabled"
    }