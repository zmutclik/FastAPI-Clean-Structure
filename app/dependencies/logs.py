from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.repositories.logs import LogsRepository as GenericRepository
from app.services.logs import LogServices as GenericService

from app.models.logs import TableLogs

# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_textual_sql.htm

DB_ENGINE = "sqlite:///./files/db/auth.db"
engine_db = create_engine(DB_ENGINE)
# conn_db = engine_db.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
SessionLocal.configure(binds={TableLogs: engine_db})


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_logs_repository(db=Depends(get_db)) -> GenericRepository:
    return GenericRepository(db)


def get_logs_services(repository=Depends(get_logs_repository)) -> GenericService:
    return GenericService(repository)
