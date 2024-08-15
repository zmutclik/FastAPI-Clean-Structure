from datetime import datetime, date
from typing import List, Annotated
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services import get_current_active_user
from ..repositories import ScopesRepository
from ..schemas import UserResponse, Scopes, ScopesSave

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


@router.post(
    "/scope",
    response_model=Scopes,
)
async def post_scope_baru(
    dataIn: ScopesSave,
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopesRepository(db).create(dataIn.model_dump())


@router.put(
    "/scope/{ID}",
    response_model=Scopes,
)
async def put_update_scope(
    ID: int,
    dataIn: ScopesSave,
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    return ScopesRepository(db).update(ID, dataIn.model_dump())


@router.post("/scope/delete", response_model=List[Scopes])
async def delete_user_scope(
    ID: int,
    current_user: Annotated[UserResponse, Security(get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db),
):
    if not ScopesRepository(db).getById(ID):
        raise HTTPException(status_code=404, detail="Data Tidak Ada.")

    ScopesRepository(db).delete(ID)
    return ScopesRepository(db).all()
