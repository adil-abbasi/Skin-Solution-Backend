from passlib.context import CryptContext
from sqlalchemy.orm import Session


from app.models.user import User
from app.schemas.user import UserLogin
from app.utils.security import create_access_token


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class AuthService:

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ):
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    @staticmethod
    def create_default_admin(db: Session):

        admin = db.query(User).filter(
            User.username == "admin"
        ).first()

        if admin:
            return

        admin = User(
            username="admin",
            password=AuthService.hash_password("admin123"),
            full_name="System Administrator",
            role="Admin"
        )

        db.add(admin)
        db.commit()

    @staticmethod
    def login(
        db: Session,
        user: UserLogin
    ):

        db_user = db.query(User).filter(
            User.username == user.username
        ).first()

        if not db_user:
            return None

        if not AuthService.verify_password(
            user.password,
            db_user.password
        ):
            return None

        token = create_access_token(
            {
                "sub": db_user.username,
                "role": db_user.role
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "full_name": db_user.full_name,
                "role": db_user.role
            }
        }

    @staticmethod
    def change_password(
        db: Session,
        username: str,
        old_password: str,
        new_password: str
    ):

        user = db.query(User).filter(
            User.username == username
        ).first()

        if not user:
            return False

        if not AuthService.verify_password(
            old_password,
            user.password
        ):
            return False

        user.password = AuthService.hash_password(
            new_password
        )

        db.commit()

        return True

    @staticmethod
    def get_user(
        db: Session,
        username: str
    ):

        return db.query(User).filter(
            User.username == username
        ).first()