from datetime import datetime, timedelta
from typing import Annotated, Union
import uuid

from fastapi import Form, Depends, APIRouter, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config
from ..core.database import get_db

from ..services import authenticate_user, verify_scope, create_user_access_token

from ..schemas import Token, TokenData


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
    access_token = create_user_access_token(db, user, form_data.scopes, True)
    return {"access_token": access_token, "token_type": "bearer"}
