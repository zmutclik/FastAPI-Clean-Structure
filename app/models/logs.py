import os

from sqlalchemy import Column, Integer, String, Date, Time, Float, DateTime

from app.dependencies.logs import Base, fileDB_ENGINE, engine_db


class TableLogs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    startTime = Column(DateTime)
    app = Column(String(100), index=True)
    platform = Column(String(100), index=True)
    browser = Column(String(100), index=True)
    path = Column(String(256), index=True)
    path_params = Column(String(256))
    method = Column(String(10), index=True)
    ipaddress = Column(String(50), index=True)
    username = Column(String(50), index=True)
    status_code = Column(Integer, index=True)
    process_time = Column(Float, nullable=True)


if os.path.exists(fileDB_ENGINE):
    file_stats = os.stat(fileDB_ENGINE)
    if file_stats.st_size == 0:
        Base.metadata.create_all(bind=engine_db)
