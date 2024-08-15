import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Dependency
def get_db():
    now = datetime.now()
    fileDB_ENGINE = "./files/data/db/logs_{}.db".format(now.strftime("%Y-%m"))
    DB_ENGINE = "sqlite:///" + fileDB_ENGINE
    engine_db = create_engine(DB_ENGINE, connect_args={"check_same_thread": False})

    if not os.path.exists(fileDB_ENGINE):
        with open(fileDB_ENGINE, "w") as f:
            f.write("")

    if os.path.exists(fileDB_ENGINE):
        file_stats = os.stat(fileDB_ENGINE)
        if file_stats.st_size == 0:
            Base.metadata.create_all(bind=engine_db)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
