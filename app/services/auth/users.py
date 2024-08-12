from datetime import datetime, timedelta
import uuid
from typing import Union, Annotated, TypeVar, Generic, Type
from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import ValidationError
from fastapi import Depends, HTTPException, Security, status, Request
from fastapi.security import SecurityScopes

from app.core.env import SECRET_TEXT, ALGORITHM
from app.schemas.auth.users import UserResponse
from app.schemas.auth.token import TokenData
from app.repositories.auth.users import UsersRepository
from app.repositories.auth.scopes import ScopesRepository


class UserServices:

    def __init__(self):
        self.repository = UsersRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate(self, username: str, password: str):
        user = self.repository.get(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_current_user(
        self, security_scopes: SecurityScopes, token: Annotated[str, Depends(ScopesRepository().oauth2_scheme)], request: Request
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
        user = self.repository.get(token_data.username)
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

    async def get_current_active_user(self, current_user: Annotated[UserResponse, Security(get_current_user, scopes=["default"])]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
