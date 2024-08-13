from datetime import datetime, timedelta
from typing import Annotated, Union
import uuid

from fastapi import Form, Depends, APIRouter, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from app.core.env import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.auth.auth import authenticate_user, verify_scope, create_access_token
from app.schemas.auth.token import Token, TokenData


########################################################################################################################
router = APIRouter(
    prefix="",
    tags=["AUTH"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) if not user.unlimited_token_expires else None
    user_scope = verify_scope(user.id, form_data.scopes)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user_scope},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
