from pydantic import UUID4

from src.users.models import User, Role
from src.users.repos.repos_roles import RoleDBRepository
from src.users.repos.repos_users import UserDBRepository
from src.users.schemas import UserCreate, UserUpdate, RoleCreate, RoleUpdate
from src.utils.security import get_password_hash, verify_password


class UserService:
    def __init__(self, db):
        self.repo = UserDBRepository(db)

    def get_user(self, user_id: int) -> User:
        return self.repo.get_user(user_id)

    def get_users(self) -> list[User]:
        return self.repo.get_users()

    def create_user(self, user: UserCreate) -> User:
        existing_user = self.repo.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        user.password = get_password_hash(user.password)
        return self.repo.create_user(user)

    def update_user(self, user: UserUpdate) -> User:
        existing_user = self.repo.get_user_by_email(user.email)
        if existing_user and existing_user.id != user.id:
            raise ValueError("User with this email already exists")
        if user.password:
            user.password = get_password_hash(user.password)
        return self.repo.update_user(user)

    def delete_user(self, user_id: UUID4) -> None:
        return self.repo.delete_user(user_id)

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.repo.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def assign_role(self, user: UserUpdate, role_id: int) -> User:
        user.role_id = role_id
        return self.repo.update_user(user)


class RoleService:
    def __init__(self, db):
        self.repo = RoleDBRepository(db)

    def get_role(self, role_id: int) -> Role:
        return self.repo.get_role(role_id)

    def get_roles(self) -> list[Role]:
        return self.repo.get_roles()

    def create_role(self, role: RoleCreate) -> Role:
        existing_role = self.repo.get_role_by_name(role.name)
        if existing_role:
            raise ValueError("Role with this name already exists")
        return self.repo.create_role(role)

    def update_role(self, role: RoleUpdate) -> Role:
        existing_role = self.repo.get_role_by_name(role.name)
        if existing_role and existing_role.id != role.id:
            raise ValueError("Role with this name already exists")
        return self.repo.update_role(role)

    def delete_role(self, role_id: int) -> None:
        return self.repo.delete_role(role_id)
