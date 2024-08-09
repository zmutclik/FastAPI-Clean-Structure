from sqlalchemy.orm import Session
from app.models.logs import TableLogs as MainTable


class LogsRepository:
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self):
        pass

    def all(self):
        pass

    def create(self, dataIn):
        data = MainTable(**dataIn)
        self.db.add(data)
        self.db.commit()

    # def update(self):
    #     pass

    # def delete(self):
    #     pass
