from fastapi import FastAPI, Request, status

from .routers_page import loginPage
from .routers import user, scope, token
from .schemas import UserSchemas
from .services import get_current_active_user, get_current_user, page_get_current_active_user
from starlette.staticfiles import StaticFiles


from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

###################################################################################################################
app = FastAPI(
    title="AUTH",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None,
)


@app.get("/")
def read_sub():
    return {"message": "Hello BOZ, ini API AUTH !"}


### Sub AUTH ###
app.include_router(token.router)
app.include_router(user.router)
app.include_router(scope.router)
app.include_router(loginPage.router)

__all__ = [
    "UserSchemas",
    "get_current_active_user",
    "page_get_current_active_user",
]
