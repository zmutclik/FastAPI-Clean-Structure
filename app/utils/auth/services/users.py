from typing import Annotated

from pydantic import ValidationError
from fastapi import Security, Depends, HTTPException, Request, status
from fastapi.security import SecurityScopes
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.env import SECRET_TEXT, ALGORITHM
from ..core.database import get_db
from ..repositories.users import UsersRepository

from ..services.scope import oauth2_scheme
from ..services.password import verify_password,get_password_hash

from ..schemas.token import TokenData
from ..schemas.users import UserResponse


def authenticate_user(username: str, password: str, db: Session):
    userrepo = UsersRepository(db)
    user = userrepo.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], request: Request, userrepo=UsersRepository(Depends(get_db))
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_TEXT, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = userrepo.get(token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    request.state.username = user.username
    return user


async def get_current_active_user(
    current_user: Annotated[UserResponse, Security(get_current_user, scopes=["default"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
