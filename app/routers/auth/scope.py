
from datetime import datetime, date
from fastapi import APIRouter, Depends,  Security
from sqlalchemy.orm import Session
# from app.database_ import get_db, conn_db
from ..database_ import get_db
from ..dependecies.auth import get_current_active_user, User
from ..cruds import ScopeCrud
### SCHEMAS ############################################################################################################
from typing import Generic, TypeVar, List, Optional, Union, Annotated, Any, Dict
from pydantic import BaseModel, Json, Field
import uuid


class scope(BaseModel):
    # uuid: uuid.UUID
    id:int
    scope: str
    desc: str


########################################################################################################################
router = APIRouter(
    prefix="",
    tags=["SCOPE"],
)


@router.get(
    "/scopes",
    response_model=List[scope],
)
async def get_scopes_list(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])],
):
    return ScopeCrud.all()


@router.get(
    "/scope/{ID}",
    response_model=scope,
)
async def get_detail_scope(
    ID: int,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopeCrud.get(db, ID)


@router.post(
    "/scope",
    response_model=scope,
)
async def post_scope_baru(
    dataIn: ScopeCrud.data_save,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopeCrud.save(db, ScopeCrud.data_save(**dataIn.model_dump()))


@router.put(
    "/scope/{ID}",
    response_model=scope,
)
async def put_update_scope(
    ID: int,
    dataIn: ScopeCrud.data_save,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopeCrud.put(db, ID, ScopeCrud.data_save(**dataIn.model_dump()))


# @router.delete(
#     "/scope/{UUID_}",
#     response_model=scope,
# )
# async def create_user(
#     UUID_: uuid.UUID,
#     current_user: Annotated[User, Security(get_current_active_user, scopes=["11111111-1111-1111-1111-111111111111"])],
#     db: Session = Depends(get_db),
# ):
#     return ScopeCrud.d(db, UUID_)
