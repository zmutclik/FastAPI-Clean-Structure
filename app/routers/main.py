from fastapi import APIRouter, Depends, Request

from starlette.responses import FileResponse

router = APIRouter()


@router.get("/")
async def root(request: Request):
    return {"message": "Hello BOZ " + request.client.host + " !!!"}


@router.get("/favicon.ico")
def favicon():
    return FileResponse("files_static/favicon.ico")
