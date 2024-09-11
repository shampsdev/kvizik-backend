from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Cat(Base):
    __tablename__ = "cat"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    is_fat = Column(Boolean, default=False)
