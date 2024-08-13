from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.dependencies.logs import get_db
from app.models.auth import ScopeTable as MainTable


class ScopesRepository:
    def __init__(self, db_session: Session) -> None:
        self.session: Session = db_session

    def oauth2_scheme(self):
        ScopeList = {}
        for item in self.all():
            ScopeList[item.scope] = item.desc
        return OAuth2PasswordBearer(
            tokenUrl="/auth/token",
            scopes=ScopeList,
        )

    def get(self, scope: str):
        return self.session.query(MainTable).filter(MainTable.scope == scope).first()

    def getById(self, id: int):
        return self.session.query(MainTable).filter(MainTable.id == id).first()

    def all(self):
        return self.session.query(MainTable).all()

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

    # def delete(self, username: str, id_delete: int):
    #     return self.update(
    #         id_delete, {"deleted_at": datetime.now(), "deleted_user": username}
    #     )
