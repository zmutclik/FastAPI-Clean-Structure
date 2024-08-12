from datetime import datetime, timedelta
import uuid
from typing import Union, Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import BaseModel, EmailStr, ValidationError
from fastapi import Depends, HTTPException, Security, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.core.env import SECRET_TEXT, ALGORITHM
from app.repositories.auth.scopes import ScopesRepository


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_TEXT, algorithm=ALGORITHM)
    return encoded_jwt
