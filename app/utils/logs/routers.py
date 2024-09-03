from typing import Annotated
import secrets
from datetime import datetime

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .schemas import DataTablesRequest, DataTablesRespondse
from .repositories import LogsRepository

###################################################################################################################
appLOGS = FastAPI(
    title="LOGS",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None,
)
templates = Jinja2Templates(directory="app/utils/logs")

security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"semut"
    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"cilik"
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@appLOGS.get("/", response_class=HTMLResponse)
async def root(request: Request, username: Annotated[str, Depends(get_current_username)]):
    return templates.TemplateResponse(request=request, name="logs.html", context={"id": id})


@appLOGS.post("/dataTables", response_model=DataTablesRespondse)
def dataTables(dataIn: DataTablesRequest, username: Annotated[str, Depends(get_current_username)]):
    content__ = response_model = DataTablesRespondse()
    content__.draw = dataIn.draw
    content__.data = []
    if dataIn.search["time_start"] is not None:
        repo = LogsRepository(datetime.strptime(dataIn.search["time_start"], "%Y-%m-%d %H:%M:%S"))

        sql_ = """ SELECT id,startTime,platform,browser,PATH,path_params,method,ipaddress,status_code FROM logs  where startTime BETWEEN \"{}\" and \"{}\" """.format(
            dataIn.search["time_start"], dataIn.search["time_end"]
        )

        if dataIn.search["ipaddress"] != "":
            sql_ = sql_ + """ and ipaddress=\"{}\" """.format(dataIn.search["ipaddress"])

        if dataIn.search["method"] != "":
            sql_ = sql_ + """ and method=\"{}\" """.format(dataIn.search["method"])

        if dataIn.search["status"] != "":
            sql_ = sql_ + """ and status_code like \"{}%\" """.format(dataIn.search["status"])

        if dataIn.search["path"] != "":
            sql_ = sql_ + """ and path like \"%{}%\" """.format(dataIn.search["path"])

        if dataIn.search["params"] != "":
            sql_ = sql_ + """ and path_params like \"%{}%\" """.format(dataIn.search["params"])

        sql_ = sql_ + " order by startTime desc"
        for item in repo.execute(text(sql_)):
            item__ = {
                "DT_RowId": item[0],
                "id": item[0],
                "startTime": item[1],
                "platform": item[2],
                "browser": item[3],
                "PATH": item[4],
                "path_params": item[5],
                "method": item[6],
                "ipaddress": item[7],
                "status_code": item[8],
            }
            content__.data.append(item__)

    return content__
