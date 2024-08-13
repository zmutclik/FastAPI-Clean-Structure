from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from auth.core.database import engine_db
from auth.repositories.users import UsersRepository
from auth.repositories.scopes import ScopesRepository

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


def verify_scope(id_user: int, scopes: list[str], db: Session):
    userRepo = UsersRepository(db)
    scopesPass = ["default"]
    scopesUser = []
    scopesUserJs = {}
    scopesUserDB = userRepo.getScopes(id_user)
    for item in scopesUserDB:
        scopesUser.append(item.scope)
        scopesUserJs[item.scope] = item.scope
    for scope in scopes:
        if scope not in scopesUser:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user scope : " + scope)
        else:
            scopesPass.append(str(scopesUserJs[scope]))
    return scopesPass
