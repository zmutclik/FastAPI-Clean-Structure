from datetime import datetime, timedelta

from fastapi import Form, Depends, APIRouter, HTTPException, Security, status
from sqlalchemy.orm import Session

# from ..cruds import UsersCrud, UserScopeCrud

# from app.database_ import get_db, conn_db
# from ..database_ import get_db
# from ..dependecies.auth import get_current_active_user, User, get_password_hash, verify_password
from app.dependencies.auth import get_db
from app.repositories.auth.users import UsersRepository

from app.utils.auth import get_current_active_user, verify_password, get_password_hash

from app.schemas.auth.users import UserResponse, UserSave

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
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return UsersRepository(db).all()


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return UsersRepository(db).getbyID(db, current_user.id)


@router.post("/users/gantipass", response_model=UserResponse)
async def ganti_password(
    password: Annotated[str, Form()],
    password_baru: Annotated[str, Form()],
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password Lama Tidak Cocok.")

    return UsersRepository(db).put(db, current_user.id, {"hashed_password": get_password_hash(password_baru)})


@router.post("/users", response_model=UserResponse)
async def create_user(
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    full_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    userrepo = UsersRepository(db)
    if userrepo.get(username):
        raise HTTPException(status_code=400, detail="Username has Used.")
    if userrepo.getbyEmail(email):
        raise HTTPException(status_code=400, detail="Email has Used.")

    hashed_password = get_password_hash(password)
    return userrepo.save(
        db,
        UserSave(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            created_user=current_user.username,
        ),
    )


@router.post("/users/scope", response_model=UserResponse)
async def create_user(
    id_user: Annotated[int, Form()],
    id_scope: Annotated[int, Form()],
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    userrepo = UsersRepository(db)
    userrepo.save(db, UserSave(id_user=id_user, id_scope=id_scope))
    return userrepo.getbyID(db, id_user)


@router.post("/users/scope/delete", response_model=UserResponse)
async def delete_user_scope(
    id: Annotated[int, Form()],
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    userrepo = UsersRepository(db)
    dataUserScope = userrepo.get(db, id)
    if not dataUserScope:
        raise HTTPException(status_code=404, detail="Data Tidak Ada.")
    dataUser = userrepo.getbyID(db, dataUserScope.id_user)

    userrepo.delete(db, id)
    return dataUser
