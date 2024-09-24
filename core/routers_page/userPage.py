from typing import Annotated, Union, Any
from enum import Enum

from fastapi import APIRouter, Request, Response, Cookie, Security, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database.auth import engine_db, get_db
from app.core import config
from core import UserSchemas, page_get_current_active_user
from core.models import auth
from core.schemas import TemplateResponseSet, TemplateResponseJSSet

from sqlalchemy import select

from datatables import DataTable
from datatables.base import DTDataCallbacks

router = APIRouter(
    prefix="/page/users",
    tags=["FORM"],
)
templates = Jinja2Templates(directory="templates")
path_template = "page/system/users/"


class PathEnum(str, Enum):
    form = "form"
    indexJs = "index.js"
    formJs = "form.js"


@router.get("/", response_class=HTMLResponse)
def page_system_users(
    request: Request,
    current_user: Annotated[UserSchemas, Depends(page_get_current_active_user)],
):
    return TemplateResponseSet(templates, path_template + "index", request)


@router.get("/{clientId}/{sessionId}/{app_version}/{pathFile}", response_class=HTMLResponse)
def page_(
    clientId: str,
    sessionId: str,
    request: Request,
    current_user: Annotated[UserSchemas, Depends(page_get_current_active_user)],
    pathFile: PathEnum,
):
    return TemplateResponseSet(templates, path_template + pathFile, request, clientId, sessionId)


@router.post("/{clientId}/{sessionId}/datatables", status_code=201)
def get_datatable_result(
    params: dict[str, Any],
    clientId: str,
    sessionId: str,
    request: Request,
) -> dict[str, Any]:
    if request.state.clientId == clientId and request.state.sessionId == sessionId:
        datatable: DataTable = DataTable(
            request_params=params,
            table=select(auth.UsersTable),
            column_names=["id", "username", "email", "full_name", "unlimited_token_expires"],
            engine=engine_db,
            # callbacks=callbacks,
        )
        return datatable.output_result()
    else:
        raise HTTPException(status_code=404)
