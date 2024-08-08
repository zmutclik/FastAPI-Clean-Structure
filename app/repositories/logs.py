from sqlalchemy.orm import Session
from fastapi import Request, Response
from datetime import datetime, date
from app.schemas.logs import dataLogs
from app.core.env import APP_NAME


class LogsRepository:
    startTime: datetime
    endTime: datetime

    def __init__(self, db: Session) -> None:
        self.db = db
        self.startTime = datetime.now()

    def create(request: Request):
        request.state.uuid = None
        request.state.username = None
        request.state.useraccess = None
