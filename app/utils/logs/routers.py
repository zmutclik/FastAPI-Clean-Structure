from typing import Annotated
from datetime import datetime

from fastapi import FastAPI, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

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
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()


@appLOGS.get("/", response_class=HTMLResponse)
async def root(request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == "semut" and credentials.password == "cilik":
        return templates.TemplateResponse(request=request, name="logs.html", context={"id": id})


@appLOGS.post("/dataTables", response_model=DataTablesRespondse)
def dataTables(dataIn: DataTablesRequest, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    content__ = response_model = DataTablesRespondse()
    content__.draw = dataIn.draw
    content__.data = []
    if credentials.username == "semut" and credentials.password == "cilik":
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
