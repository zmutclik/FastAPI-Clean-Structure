from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
# from app.database_ import get_db
from datetime import datetime, date
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, HTMLResponse
# from key_generator.key_generator import generate

# from app.cruds import DeviceCrud

router = APIRouter()


@router.get("/")
async def root(request: Request):
# def root(request: Request, db: Session = Depends(get_db)):
    # client_ip = DeviceCrud.get(db, request.client.host)
    for item in request.headers:
        try:
            await print(item," -- ",request.headers.get(item))
        except :
            pass
        
    return {"message": "Hello BOZ "+request.client.host+" !!!"}


@router.get('/favicon.ico')
def favicon():
    return FileResponse("files_static/favicon.ico")
