from sqlalchemy import create_engine
<<<<<<< HEAD:app/db/database.py
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import POSTGRES_DB_URI

engine = create_engine(POSTGRES_DB_URI)
=======
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(str(settings.POSTGRES_DATABASE_URI))
>>>>>>> 9ef326e (Migrate to pydantic settings):app/database.py


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
