from typing import Annotated, Union

from fastapi import APIRouter, Request, Response, Cookie, Security
from starlette.responses import FileResponse
from app.utils.auth import UserSchemas, get_current_user

router = APIRouter()


@router.get("/")
async def root(request: Request):
    return {"message": "Hello BOZ " + request.client.host + " !!!"}


@router.get("/me")
async def root(request: Request, current_user: Annotated[UserSchemas, Security(get_current_user, scopes=[])]):
    return {"message": "Hello BOZ " + current_user.username + "@" + request.client.host + " !!!"}


@router.get("/favicon.ico")
def favicon():
    return FileResponse("files_static/favicon.ico")
