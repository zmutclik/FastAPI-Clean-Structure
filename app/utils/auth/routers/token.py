from datetime import datetime, timedelta
from typing import Annotated, Union
import uuid

from fastapi import Form, Depends, APIRouter, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.env import ACCESS_TOKEN_EXPIRE_MINUTES
from ..core.database import get_db

from ..services.users import authenticate_user
from ..services.scope import verify_scope
from ..services.password import create_access_token

from ..schemas.token import Token, TokenData


########################################################################################################################
router = APIRouter(
    prefix="",
    tags=["AUTH"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) if not user.unlimited_token_expires else None
    user_scope = verify_scope(user.id, form_data.scopes, db)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user_scope},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
