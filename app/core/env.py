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
# to get a string like this run:
# openssl rand -hex 32
SECRET_TEXT = os.environ.get("SECRET_TEXT", "HxekWSNWYKyOsezYRQxFEJNgbUroNzDT")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM = "HS256"
#######################################################################################################################
DB_IPADDRESS = os.environ.get("DB_IPADDRESS", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "3307")
DB_NAME = os.environ.get("DB_NAME", "db")
DB_USER = os.environ.get("DB_APPUSER", "root")
DB_PASS = os.environ.get("DB_APPPASS", "blackant")

DB_ENGINE = "mysql+pymysql://{user}:{password}@{hostname}:{port}/{database}".format(
    user=DB_USER,
    port=DB_PORT,
    password=DB_PASS,
    hostname=DB_IPADDRESS,
    database=DB_NAME,
)
#######################################################################################################################
RABBITMQ_IPADDRESS = os.environ.get("RMQ_IPADDRESS", "192.168.40.5")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "semut")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", "5672")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "blackant")
RABBITMQ_VHOST = os.environ.get("RABBITMQ_VHOST", "semut-dev")

CELERY_BROKER_URL = "amqp://{user}:{password}@{hostname}:{ports}//{vhost}".format(
    user=RABBITMQ_USER,
    password=RABBITMQ_PASS,
    hostname=RABBITMQ_IPADDRESS,
    ports=RABBITMQ_PORT,
    vhost=RABBITMQ_VHOST,
)
#######################################################################################################################
