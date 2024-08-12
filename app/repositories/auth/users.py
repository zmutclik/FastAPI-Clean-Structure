from datetime import datetime
from typing import Union, Annotated, TypeVar, Generic, Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.logs import get_db
from app.dependencies.auth import Base
from app.models.auth import UsersTable as MainTable


ModelType = TypeVar("ModelType", bound=Base)


class UsersRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession) -> None:
        self.session = db_session
        self.model_class: Type[ModelType] = model

    def get(self, username: str):
        return self.session.query(MainTable).filter(MainTable.username == username).first()

    def getById(self, id: int):
        return self.session.query(MainTable).filter(MainTable.id == id).first()

    def getByEmail(self, email: str):
        return self.session.queue(MainTable).filter(MainTable.email == email).first()

    def getScopes(self, id: int):
        return self.session.query(MainTable.SCOPES).filter(MainTable.id == id).first()

    def all(self):
        return self.session.query(MainTable).filter(MainTable.deleted_at != None).order_by(MainTable.username).all()

    def create(self, dataIn):
        data = MainTable(**dataIn)
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def update(self, id: int, dataIn: dict):
        dataIn_update = dataIn if type(dataIn) is dict else dataIn.__dict__
        (self.session.query(MainTable).filter(MainTable.id == id).update(dataIn_update))
        self.session.commit()
        return self.getById(id)

    def delete(self, username: str, id_delete: int):
        return self.update(id_delete, {"deleted_at": datetime.now(), "deleted_user": username})
