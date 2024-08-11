from datetime import datetime
from sqlalchemy.orm import Session

from app.dependencies.logs import get_db
from app.models.auth import ScopeTable as MainTable


class ScopesRepository:
    def __init__(self) -> None:
        self.db: Session = get_db().__next__()

    def get(self, scope: str):
        return self.db.query(MainTable).filter(MainTable.scope == scope).first()

    def getById(self, id: int):
        return self.db.query(MainTable).filter(MainTable.id == id).first()

    def all(self):
        return self.db.query(MainTable).order_by(MainTable.scope).all()

    def create(self, dataIn):
        data = MainTable(**dataIn)
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def update(self, id: int, dataIn: dict):
        dataIn_update = dataIn if type(dataIn) is dict else dataIn.__dict__
        (self.db.query(MainTable).filter(MainTable.id == id).update(dataIn_update))
        self.db.commit()
        return self.getById(id)

    # def delete(self, username: str, id_delete: int):
    #     return self.update(
    #         id_delete, {"deleted_at": datetime.now(), "deleted_user": username}
    #     )
