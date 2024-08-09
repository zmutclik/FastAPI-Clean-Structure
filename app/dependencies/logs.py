import os
from datetime import datetime
from typing import TypeVar

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.repositories.logs import LogsRepository
from app.services.logs import LogServices

from app.models.logs import Base

now = datetime.now()
fileDB_ENGINE = "./files/data/db/logs_{}.db".format(now.strftime("%Y-%m"))
DB_ENGINE = "sqlite:///" + fileDB_ENGINE

if not os.path.exists(fileDB_ENGINE):
    with open(fileDB_ENGINE, "w") as f:
        f.write("")

engine_db = create_engine(DB_ENGINE, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)

if os.path.exists(fileDB_ENGINE):
    file_stats = os.stat(fileDB_ENGINE)
    if file_stats.st_size == 0:
        Base.metadata.create_all(bind=engine_db)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_logs_repository(db=Depends(get_db)):
    return LogsRepository(db)


def get_logs_services(repository=Depends(get_logs_repository)):
    return LogServices(repository)
