from typing import Annotated, Union
import json

from fastapi import APIRouter, Request, Response, Cookie, Security, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates

from app.core import config

router = APIRouter(
    prefix="",
    tags=["FORM"],
)
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home/login.html",
        context={
            "app_name": config.APP_NAME,
        },
    )
