from contextlib import contextmanager
from typing import Generator

from src.auth.schemas import TokenPayload
from src.database.session import SessionLocal
from collections.abc import Generator
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from src.config import settings
from src.users.models import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


def get_current_user(security_scopes: SecurityScopes, db: Session = Depends(get_db),
                     token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).get(token_data.sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if security_scopes.scopes:
        if user.role.name not in security_scopes.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
            )
    return user
