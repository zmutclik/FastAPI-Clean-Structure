from datetime import datetime, timedelta
import uuid
from typing import Union, Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import BaseModel, EmailStr, ValidationError
from fastapi import Depends, HTTPException, Security, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.core.env import SECRET_TEXT, ACCESS_TOKEN_EXPIRE_MINUTES
from app.repositories.auth.scopes import ScopesRepository


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = SECRET_TEXT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
scopes = ScopesRepository()

ScopeList = {}
for item in scopes.all():
    ScopeList[item.scope] = item.desc

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes=ScopeList,
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = UsersCrud.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = UsersCrud.get(token_data.username)
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
    current_user: Annotated[User, Security(get_current_user, scopes=["default"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def verify_scope(id_user: int, scopes: list[str]):
    scopesPass = ["default"]
    scopesUser = []
    scopesUserJs = {}
    scopesUserDB = UserScopeCrud.all(id_user)
    for item in scopesUserDB:
        scopesUser.append(item.scope)
        scopesUserJs[item.scope] = item.scope
    for scope in scopes:
        if scope not in scopesUser:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user scope : " + scope,
            )
        else:
            scopesPass.append(str(scopesUserJs[scope]))
    return scopesPass
