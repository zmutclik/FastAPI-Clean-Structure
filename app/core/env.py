import os
from os.path import join
from dotenv import load_dotenv

pathfile = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep)
pathfile = os.path.abspath(os.path.join(pathfile, ".."))
dotenv_path = join(pathfile, ".env")

load_dotenv(dotenv_path)

#######################################################################################################################
APP_NAME = os.environ.get("APP_NAME", "FastAPI-Clean-Structure")
APP_DESCRIPTIOIN = os.environ.get(
    "APP_DESCRIPTIOIN",
    "This is a very fancy project, with auto docs for the API and everything.",
)

SECRET_TEXT = os.environ.get("SECRET_TEXT", "HxekWSNWYKyOsezYRQxFEJNgbUroNzDT")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
#######################################################################################################################
