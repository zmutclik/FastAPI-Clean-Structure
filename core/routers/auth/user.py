from fastapi import Form, Depends, APIRouter, HTTPException, Security, status
from sqlalchemy.orm import Session

from ...database.auth import get_db
from ...repositories.auth import UsersRepository, UserScopesRepository

from ...services.auth import get_current_active_user, verify_password, get_password_hash

from ...schemas.auth import UserResponse, UserSave, UserSchemas, UserScopesSave

### SCHEMAS ############################################################################################################
from typing import Generic, TypeVar, List, Optional, Union, Annotated, Any, Dict
from pydantic import BaseModel, Json, Field, EmailStr
import uuid


########################################################################################################################
router = APIRouter(
    prefix="",
    tags=["USERS"],
)


@router.get("/users/list", response_model=List[UserResponse])
async def read_users_list(
    current_user: Annotated[UserSchemas, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return UsersRepository(db).all()


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserSchemas, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return UsersRepository(db).getById(current_user.id)


@router.post("/users/gantipass", response_model=UserResponse)
async def ganti_password(
    password: Annotated[str, Form()],
    password_baru: Annotated[str, Form()],
    current_user: Annotated[UserSchemas, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password Lama Tidak Cocok.")

    password_baru = get_password_hash(password_baru)
    return UsersRepository(db).update(current_user.id, {"hashed_password": password_baru})


@router.post("/users", response_model=UserResponse)
async def create_user(
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    full_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    current_user: Annotated[UserSchemas, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    userrepo = UsersRepository(db)
    if userrepo.get(username):
        raise HTTPException(status_code=400, detail="Username has Used.")
    if userrepo.getByEmail(email):
        raise HTTPException(status_code=400, detail="Email has Used.")

    hashed_password = get_password_hash(password)
    data = UserSave(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        created_user=current_user.username,
    )
    return userrepo.create(data.model_dump())


@router.post("/users/scope", response_model=UserResponse)
async def create_user(
    id_user: Annotated[int, Form()],
    id_scope: Annotated[int, Form()],
    current_user: Annotated[UserSchemas, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    userrepo = UserScopesRepository(db)
    dataSave = UserScopesSave(id_user=id_user, id_scope=id_scope)
    userscope = userrepo.create(dataSave.model_dump())
    return UsersRepository(db).getById(id_user)


@router.post("/users/scope/delete", response_model=UserResponse)
async def delete_user_scope(
    id_user: Annotated[int, Form()],
    id_user_scope: Annotated[int, Form()],
    current_user: Annotated[UserSchemas, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    userrepo = UserScopesRepository(db)
    if not userrepo.getByUser(id_user):
        raise HTTPException(status_code=404, detail="User Tidak Ada.")
    if not userrepo.get(id_user_scope):
        raise HTTPException(status_code=404, detail="Data Tidak Ada.")

    userrepo.delete(id_user_scope)
    return UsersRepository(db).getById(id_user)
