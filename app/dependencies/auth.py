import os
from datetime import datetime
from typing import TypeVar

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
now = datetime.now()
fileDB_ENGINE = "./files/data/db/logs_auth.db"
DB_ENGINE = "sqlite:///" + fileDB_ENGINE

engine_db = create_engine(DB_ENGINE, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
