from sqlalchemy.orm import Session

from .database import get_db
from .models import TableLogs as MainTable


class LogsRepository:
    def __init__(self) -> None:
        self.db: Session = get_db().__next__()
        pass

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
