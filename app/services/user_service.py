from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate
)

from app.services.auth_service import AuthService



class UserService:



    @staticmethod
    def get_all(db: Session):

        return db.query(User).all()



    @staticmethod
    def create(
        db: Session,
        user: UserCreate
    ):


        existing = db.query(User).filter(
            User.username == user.username
        ).first()


        if existing:
            return None



        db_user = User(

            username=user.username,

            password=AuthService.hash_password(
                user.password
            ),

            full_name=user.full_name,

            role=user.role

        )


        db.add(db_user)

        db.commit()

        db.refresh(db_user)


        return db_user




    @staticmethod
    def update(
        db: Session,
        user_id:int,
        data:UserUpdate
    ):


        user = db.query(User).filter(
            User.id == user_id
        ).first()


        if not user:
            return None



        for key,value in data.model_dump(
            exclude_unset=True
        ).items():

            setattr(
                user,
                key,
                value
            )


        db.commit()

        db.refresh(user)


        return user




    @staticmethod
    def change_password(
        db:Session,
        user_id:int,
        password:str
    ):


        user = db.query(User).filter(
            User.id == user_id
        ).first()


        if not user:
            return False



        user.password = AuthService.hash_password(
            password
        )


        db.commit()


        return True




    @staticmethod
    def delete(
        db:Session,
        user_id:int
    ):


        user = db.query(User).filter(
            User.id == user_id
        ).first()


        if not user:
            return None


        user.is_active=False

        db.commit()


        return user