from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config.settings import settings

engine = create_engine(settings.database_url, echo=settings.echo_sql, pool_pre_ping=True)

SesionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()


SesionDB = Annotated[Session, Depends(get_db)]