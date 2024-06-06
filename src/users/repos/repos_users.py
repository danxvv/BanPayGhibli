from abc import ABC, abstractmethod
from src.users.models import User
from sqlalchemy.orm import Session
from src.users.schemas import UserCreate, UserUpdate
from pydantic import UUID4
from sqlalchemy import select


class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: UUID4) -> User:
        pass

    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_users(self) -> list[User]:
        pass

    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    def update_user(self, user: UserUpdate) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: UUID4) -> None:
        pass


class UserDBRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: UUID4) -> User:
        return self.db.execute(select(User).where(User.id == user_id)).scalar_one()

    def get_user_by_email(self, email: str) -> User:
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_users(self) -> list[User]:
        return self.db.execute(select(User)).scalars().all()

    def create_user(self, user: UserCreate) -> User:
        user_data = user.dict()
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user: UserUpdate) -> User:
        user_data = user.dict(exclude_unset=True)
        db_user = self.get_user(user.id)
        for field in user_data:
            if field in user_data:
                setattr(db_user, field, user_data[field])
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: UUID4) -> None:
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()


