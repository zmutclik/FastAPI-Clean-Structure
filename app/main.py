from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.staticfiles import StaticFiles
from app.utils.files import getFile
from app.core.env import APP_NAME, APP_DESCRIPTIOIN


# from app.libs.logs import createLogs, ComplateLogs
# from app.libs.auth import auth
# from app.routers.admin import admin


from app.routers import (
    main,
)


def create_app() -> FastAPI:
    current_app = FastAPI(
        title=APP_NAME,
        description=APP_DESCRIPTIOIN,
        version="1.0.0",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        redoc_url=None,
        docs_url=None,
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


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html_cdn():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        # swagger_ui_dark.css CDN link
        swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css",
    )


# app.mount("/auth", auth.app)
# app.mount("/admin", admin.app)

###################################################################################################################
### STATIC ###
app.mount("/static", StaticFiles(directory="files_static", html=False), name="static")

### MAIN ###
app.include_router(main.router)
# app.include_router(files_create.router)

###################################################################################################################


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     dataLogs = await createLogs(request)
#     response = await call_next(request)
#     dataLogs = await ComplateLogs(dataLogs, request, response)
#     response.headers["X-Process-Time"] = str(dataLogs.process_time)
#     return response
