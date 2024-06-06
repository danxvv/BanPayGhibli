from fastapi import Depends, HTTPException, APIRouter, Security
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_current_user
from .services import UserService, RoleService
from .schemas import UserCreate, UserUpdate, User, Role, RoleCreate, UserUpdateRequest
from pydantic import UUID4

users_router = APIRouter()


@users_router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)


@users_router.get("/", response_model=list[User])
def read_users(db: Session = Depends(get_db), current_user: User = Security(get_current_user, scopes=["admin"])):
    user_service = UserService(db)
    return user_service.get_users()


@users_router.get("/{user_id}", response_model=User)
def read_user(user_id: UUID4, db: Session = Depends(get_db), current_user: User = Security(get_current_user)):
    if current_user.id != user_id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user_service = UserService(db)
    return user_service.get_user(user_id)


@users_router.put("/{user_id}", response_model=User)
def update_user(user: UserUpdateRequest, user_id: UUID4,
                db: Session = Depends(get_db),
                current_user: User = Security(get_current_user)):
    if current_user.id != user_id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user_service = UserService(db)
    user_update = UserUpdate(id=user_id, **user.model_dump(exclude_unset=True))
    return user_service.update_user(user_update)


@users_router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID4, db: Session = Depends(get_db),
                current_user: User = Security(get_current_user, scopes=["admin"])):
    user_service = UserService(db)
    user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}


@users_router.post("/roles/", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db),
                current_user: User = Security(get_current_user, scopes=["admin"])):
    role_service = RoleService(db)
    return role_service.create_role(role)


@users_router.get("/roles/", response_model=list[Role])
def read_roles(db: Session = Depends(get_db), current_user: User = Security(get_current_user, scopes=["admin"])):
    role_service = RoleService(db)
    return role_service.get_roles()


@users_router.post("/{user_id}/roles/{role_id}", status_code=204)
def assign_role(user_id: UUID4, role_id: int, db: Session = Depends(get_db),
                current_user: User = Security(get_current_user, scopes=["admin"])):
    user_service = UserService(db)
    user_service.assign_role(user_id, role_id)
    return {"message": "Role assigned successfully"}
