from datetime import datetime

from sqlalchemy.orm import Session

from src.db.postgresql.interfaces.user import UserRepositoryInterface
from src.db.postgresql.models.user import User as UserDB
from src.schemas.user import User, UserCredentials, UserInput


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db: Session = db

    def add(self, user: UserInput) -> User:
        now = datetime.now()
        db_user = UserDB(
            name=user.name,
            email=user.email,
            hashed_password=user.password,
            is_admin=user.is_admin,
            is_reader=user.is_reader,
            is_editor=user.is_editor,
            created_at=now,
            updated_at=now,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user = User.model_validate(db_user)
        return user

    def get_by_email(self, email: str) -> User | None:
        db_user = self.db.query(UserDB).filter(UserDB.email == email).first()
        user = User.model_validate(db_user) if db_user else None
        return user

    def get_by_id(self, user_id: str) -> User | None:
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        user = User.model_validate(db_user) if db_user else None
        return user

    def validate_credentials(
        self, user_credentials: UserCredentials
    ) -> User | None:
        db_user = (
            self.db.query(UserDB)
            .filter(
                UserDB.email == user_credentials.email,
                UserDB.hashed_password == user_credentials.password,
            )
            .first()
        )
        user = User.model_validate(db_user) if db_user else None
        return user

    def list_users(self, limit: int, offset: int) -> list[User]:
        db_users = self.db.query(UserDB).offset(offset).limit(limit).all()
        users = [User.model_validate(db_user) for db_user in db_users]
        return users

    def delete_user(self, user: User) -> bool:
        user = self.get_by_id(user.id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def update_user(self, user_id: str, **kwargs) -> User | None:
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if db_user is None:
            return None
        for key, value in kwargs.items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        user = User.model_validate(db_user)
        return user
