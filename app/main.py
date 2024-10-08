from typing import Annotated

from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.utils.files import getFile
from app.core import config

from core import LogServices, main_logs, main_auth, routers_page as core_page


from app import routers, routers_page


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


app.mount("/auth", main_auth.app)
app.mount("/logs", main_logs.app)

###################################################################################################################
### STATIC ###
app.mount("/static", StaticFiles(directory="files_static", html=False), name="static")

### MAIN API ###
app.include_router(routers.mainRouter)

### MAIN PAGE ###
app.include_router(routers_page.dashboardPageRouter)
app.include_router(core_page.userPage.router)

###################################################################################################################


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logs = LogServices(config.CLIENTID_KEY, config.SESSION_KEY, config.APP_NAME)
    await logs.start(request)
    response = await call_next(request)
    await logs.finish(request, response)
    return response


###################################################################################################################
from fastapi.responses import RedirectResponse
from app.Exceptions import RequiresLoginException


@app.exception_handler(RequiresLoginException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(_.nextRouter)
