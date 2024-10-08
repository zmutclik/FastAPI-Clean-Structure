from typing import Annotated, Union
import json
from time import sleep

from fastapi import APIRouter, Request, Response, Cookie, Security, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core import config
from ...database.auth import get_db

from ...repositories.auth import UsersRepository, ScopesRepository
from ...services.auth import authenticate_user, create_cookie_access_token
from ...schemas.auth import loginSchemas

router = APIRouter(
    prefix="",
    tags=["FORM"],
)
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def form_login(request: Request, next: str = None):
    return templates.TemplateResponse(
        request=request,
        name="core/auth/login/login.html",
        context={"app_name": config.APP_NAME, "clientId": request.state.clientId, "sessionId": request.state.sessionId, "nextpage": next},
    )


@router.get("/{clientId}/{sessionId}/login.js")
def js_login(clientId: str, sessionId: str, request: Request, next: str = None):
    if next is None:
        next = "/page/dashboard"
    if request.state.clientId == clientId and request.state.sessionId == sessionId:
        return templates.TemplateResponse(
            request=request,
            name="core/auth/login/login.js",
            media_type="application/javascript",
            context={"clientId": request.state.clientId, "sessionId": request.state.sessionId, "nextpage": next},
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
