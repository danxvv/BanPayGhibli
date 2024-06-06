from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .schemas import Token
from src.dependencies import get_db
from src.users.services import UserService
from ..config import settings
from ..utils.security import create_access_token

auth_router = APIRouter()


@auth_router.post("/login/access-token")
def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       db: Session = Depends(get_db)
                       ) -> Token:
    crud = UserService(db)
    user = crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
