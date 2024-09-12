from typing import Annotated, Union
import json
from time import sleep

from fastapi import APIRouter, Request, Response, Cookie, Security, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core import config
from ..core.database import get_db

from ..repositories import UsersRepository, ScopesRepository
from ..services import authenticate_user, create_cookie_access_token
from ..schemas import loginSchemas

router = APIRouter(
    prefix="",
    tags=["FORM"],
)
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def form_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login/login.html",
        context={"app_name": config.APP_NAME, "clientId": request.state.clientId, "sessionId": request.state.sessionId},
    )


@router.get("/{clientId}/{sessionId}/login.js")
def js_login(clientId: str, sessionId: str, request: Request):
    if request.state.clientId == clientId and request.state.sessionId == sessionId:
        return templates.TemplateResponse(
            request=request,
            name="auth/login/login.js",
            media_type="application/javascript",
            context={"clientId": request.state.clientId, "sessionId": request.state.sessionId},
        )
    else:
        raise HTTPException(status_code=404)


@router.post("/{clientId}/{sessionId}/login", status_code=201)
def post_login(
    dataIn: loginSchemas,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    userrepo = UsersRepository(db)
    user = userrepo.getByEmail(dataIn.email)
    sleep(1)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    userreal = authenticate_user(user.username, dataIn.password, db)
    if not userreal:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    create_cookie_access_token(db, response, user)
