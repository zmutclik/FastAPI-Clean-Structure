from typing import Annotated, Union
import json
from time import sleep

from fastapi import APIRouter, Request, Response, Cookie, Security, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core import config

router = APIRouter(
    prefix="",
    tags=["FORM"],
)
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
def form_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard/index2.html",
        context={"app_name": config.APP_NAME, "clientId": request.state.clientId, "sessionId": request.state.sessionId},
    )
