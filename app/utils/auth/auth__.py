from datetime import datetime, timedelta
import uuid
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Union, Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Security, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session

from app.core.env import SECRET_TEXT, ALGORITHM

from app.utils.auth.core.auth import engine_db, get_db
from app.utils.auth.repositories.users import UsersRepository
from app.utils.auth.repositories.scopes import ScopesRepository

from app.schemas.auth.users import UserResponse
from app.schemas.auth.token import TokenData

########################################################################################################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ScopeList = {}
with engine_db.begin() as connection:
    with Session(bind=connection) as db:
        scope = ScopesRepository(db)
        for item in scope.all():
            ScopeList[item.scope] = item.desc

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes=ScopeList,
)



def verify_scope(id_user: int, scopes: list[str]):
    user = UsersRepository()
    scopesPass = ["default"]
    scopesUser = []
    scopesUserJs = {}
    scopesUserDB = user.getScopes(id_user)
    for item in scopesUserDB:
        scopesUser.append(item.scope)
        scopesUserJs[item.scope] = item.scope
    for scope in scopes:
        if scope not in scopesUser:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user scope : " + scope)
        else:
            scopesPass.append(str(scopesUserJs[scope]))
    return scopesPass
