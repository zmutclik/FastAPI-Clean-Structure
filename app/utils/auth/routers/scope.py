from datetime import datetime, date
from typing import List, Annotated
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from ..core.database import get_db

from ..services.users import get_current_active_user

from ..repositories.scopes import ScopesRepository

from ..schemas.users import UserResponse
from ..schemas.scope import Scopes, ScopesSave

########################################################################################################################
router = APIRouter(
    prefix="",
    tags=["SCOPE"],
)


@router.get(
    "/scopes",
    response_model=List[Scopes],
)
async def get_scopes_list(
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopesRepository(db).all()


@router.get(
    "/scope/{ID}",
    response_model=UserResponse,
)
async def get_detail_scope(
    ID: int,
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopesRepository(db).get(db, ID)


@router.post(
    "/scope",
    response_model=UserResponse,
)
async def post_scope_baru(
    dataIn: ScopesSave,
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopesRepository(db).save(db, ScopesSave(**dataIn.model_dump()))


@router.put(
    "/scope/{ID}",
    response_model=UserResponse,
)
async def put_update_scope(
    ID: int,
    dataIn: ScopesSave,
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopesRepository(db).put(db, ID, ScopesSave(**dataIn.model_dump()))


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
