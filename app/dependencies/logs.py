import os
from datetime import datetime
from typing import TypeVar

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

now = datetime.now()
fileDB_ENGINE = "./files/data/db/logs_{}.db".format(now.strftime("%Y-%m"))
DB_ENGINE = "sqlite:///" + fileDB_ENGINE

if not os.path.exists(fileDB_ENGINE):
    with open(fileDB_ENGINE, "w") as f:
        f.write("")

engine_db = create_engine(DB_ENGINE, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
