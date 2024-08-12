import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from app.dependencies.auth import Base, fileDB_ENGINE, engine_db


class ScopeTable(Base):
    __tablename__ = "scopes"

    id = Column(Integer, primary_key=True, index=True)
    scope = Column(String(32), unique=True, index=True)
    desc = Column(String(250))

    USERCOPES = relationship("UserScopeTable", back_populates="SCOPES")


class UsersTable(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    full_name = Column(String(50))
    hashed_password = Column(String(256))
    unlimited_token_expires = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    created_user = Column(String(50), nullable=False)
    deleted_user = Column(String(50))

    SCOPES = relationship("UserScopeTable", back_populates="USER")


class UserScopeTable(Base):
    __tablename__ = "user_scopes"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id"), index=True)
    id_scope = Column(Integer, ForeignKey("scopes.id"), index=True)

    USER = relationship("UsersTable", back_populates="SCOPES")
    SCOPES = relationship("ScopeTable", back_populates="USERCOPES")

    @hybrid_property
    def scope(self) -> str:
        return self.SCOPES.scope


if not os.path.exists(fileDB_ENGINE):
    with open(fileDB_ENGINE, "w") as f:
        f.write("")

if os.path.exists(fileDB_ENGINE):
    file_stats = os.stat(fileDB_ENGINE)
    if file_stats.st_size == 0:
        Base.metadata.create_all(bind=engine_db)
        with engine_db.begin() as connection:
            with Session(bind=connection) as db:
                data = UsersTable(
                    **{
                        "username": "admin",
                        "email": "admin@test.id",
                        "full_name": "Admin SeMuT",
                        "hashed_password": "$2b$12$ofIPPqnjPf54SzEvctr3DOzNqyjZQqDaA3GraVDvBobo/UfjtGqQm",
                        "unlimited_token_expires": True,
                        "created_user": "admin",
                    }
                )
                db.add(data)
                data = ScopeTable(
                    **{
                        "scope": "admin",
                        "desc": "Privilage Khusus ADMIN",
                    }
                )
                db.add(data)
                data = UserScopeTable(
                    **{
                        "id_user": 1,
                        "id_scope": 1,
                    }
                )
                db.add(data)
                db.commit()
