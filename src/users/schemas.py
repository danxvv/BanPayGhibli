from pydantic import BaseModel, UUID4, ConfigDict
import datetime


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    role_id: int


class UserUpdate(UserBase):
    id: UUID4
    email: str | None = None
    name: str | None = None
    password: str | None = None
    role_id: int | None = None


class UserUpdateRequest(BaseModel):
    name: str | None = None
    password: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    created_at: datetime.datetime
    updated_at: datetime.datetime
    role_id: int
    role: "Role"


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
