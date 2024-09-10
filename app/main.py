from typing import Annotated

from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.utils.files import getFile
from app.core import config

from app.utils import auth
from app.utils.logs import LogServices, appLOGS


from app.routers import (
    main,
)


def create_app() -> FastAPI:
    current_app = FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        version="1.0.0",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        redoc_url=None,
        # docs_url=None,
    )

    return current_app


app = create_app()

app.router.redirect_slashes = False

origins = getFile("data/referensi/", "cross_middleware_origin")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/auth", auth.app)
app.mount("/logs", appLOGS)

###################################################################################################################
### STATIC ###
app.mount("/static", StaticFiles(directory="files_static", html=False), name="static")

### MAIN ###
app.include_router(main.router)

###################################################################################################################


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     logs = LogServices()
#     await logs.start(request)
#     response = await call_next(request)
#     await logs.finish(request, response)
#     return response
