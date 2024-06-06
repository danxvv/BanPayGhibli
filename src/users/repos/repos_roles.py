from abc import ABC, abstractmethod
from src.users.models import Role
from sqlalchemy.orm import Session
from src.users.schemas import RoleCreate, RoleUpdate
from sqlalchemy import select


class RoleRepository(ABC):
    @abstractmethod
    def get_role(self, role_id: int) -> Role:
        pass

    def get_role_by_name(self, name: str) -> Role:
        pass

    @abstractmethod
    def get_roles(self) -> list[Role]:
        pass

    @abstractmethod
    def create_role(self, role: RoleCreate) -> Role:
        pass

    @abstractmethod
    def update_role(self, role: RoleUpdate) -> Role:
        pass

    @abstractmethod
    def delete_role(self, role_id: int) -> None:
        pass


class RoleDBRepository(RoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_role(self, role_id: int) -> Role:
        return self.db.execute(select(Role).where(Role.id == role_id)).scalar_one()

    def get_role_by_name(self, name: str) -> Role:
        return self.db.execute(select(Role).where(Role.name == name)).scalar_one_or_none()

    def get_roles(self) -> list[Role]:
        return self.db.execute(select(Role)).scalars().all()

    def create_role(self, role: RoleCreate) -> Role:
        role_data = role.dict()
        db_role = Role(**role_data)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def update_role(self, role: RoleUpdate) -> Role:
        role_data = role.dict(exclude_unset=True)
        db_role = self.get_role(role.id)
        for field in role_data:
            if field in role_data:
                setattr(db_role, field, role_data[field])
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def delete_role(self, role_id: int) -> None:
        db_role = self.get_role(role_id)
        self.db.delete(db_role)
        self.db.commit()
