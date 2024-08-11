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


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
