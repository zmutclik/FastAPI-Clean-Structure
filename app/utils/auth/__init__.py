from fastapi import FastAPI
from .routers import user, scope, token,login
from .schemas import UserSchemas
from .services import get_current_active_user,get_current_user
from starlette.staticfiles import StaticFiles

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
app.include_router(login.router)

__all__ = [
    "UserSchemas",
    "get_current_active_user",
]
