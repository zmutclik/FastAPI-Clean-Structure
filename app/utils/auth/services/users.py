from typing import Annotated
from datetime import timedelta

from pydantic import ValidationError
from fastapi import Security, Depends, HTTPException, Request, status, Response
from fastapi.responses import RedirectResponse
from fastapi.security import SecurityScopes
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core import config
from ..core.database import get_db, engine_db
from ..repositories import UsersRepository, ScopesRepository

from ..services.scope import oauth2_scheme, verify_scope
from ..services.password import verify_password, get_password_hash, create_access_token

from ..schemas.token import TokenData
from ..schemas.users import UserResponse
from app.Exceptions import RequiresLoginException


def credentials_exception(authenticate_detail: str, authenticate_value: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=authenticate_detail,
        headers={"WWW-Authenticate": authenticate_value},
    )


def authenticate_user(username: str, password: str, db: Session):
    userrepo = UsersRepository(db)
    user = userrepo.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def decode_token(token: str, exception):
    try:
        payload = jwt.decode(token, config.SECRET_TEXT, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise exception

    return token_data


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], request: Request):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    token_data = decode_token(token, credentials_exception("Could not validate credentials", authenticate_value))

    with engine_db.begin() as connection:
        with Session(bind=connection) as db:
            user = UsersRepository(db).get(token_data.username)
            if user is None:
                raise credentials_exception("Could not validate credentials", authenticate_value)
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise credentials_exception("Not enough permissions", authenticate_value)

            request.state.username = user.username
            return user


async def get_current_active_user(current_user: Annotated[UserResponse, Security(get_current_user, scopes=["default"])]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def page_get_current_active_user(request: Request):
    token = request.cookies.get(config.TOKEN_KEY)
    if token is None:
        raise RequiresLoginException(f"/login")
    token_data = decode_token(token, RequiresLoginException(f"/login"))

    with engine_db.begin() as connection:
        with Session(bind=connection) as db:
            user = UsersRepository(db).get(token_data.username)
            if user is None:
                raise RequiresLoginException(f"/login")

            request.state.username = user.username
            return user


def create_user_access_token(db: Session, userModel, userScope, unlimited_token: bool = False) -> str:
    access_token_expires = None if userModel.unlimited_token_expires and unlimited_token else timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    user_scope = verify_scope(userModel.id, userScope, db)
    access_token = create_access_token(
        data={"sub": userModel.username, "scopes": user_scope},
        expires_delta=access_token_expires,
    )
    return access_token


def create_cookie_access_token(db: Session, response: Response, userModel):
    userScope = []
    for item in ScopesRepository(db).getScopesUser(userModel.id):
        userScope.append(item.scope)
    access_token = create_user_access_token(db, userModel, userScope)
    response.set_cookie(key=config.TOKEN_KEY, value=access_token)
