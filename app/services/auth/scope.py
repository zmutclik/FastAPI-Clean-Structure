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
from app.repositories.auth.users import UsersRepository



class ScopeServices:
    def __init__(self):
        self.ScopesRepository = ScopesRepository()
        self.UsersRepository = UsersRepository()

    def get_all_user(self, id: int):
        self.UsersRepository.getScopes(id)

    def verify(self, id_user: int, scopes: list[str]):
        scopesPass = ["default"]
        scopesUser = []
        scopesUserJs = {}
        scopesUserDB = self.get_all_user(id_user)
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
