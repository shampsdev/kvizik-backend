from sqlalchemy.orm import Session

from . import models, schemas


def get_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()


def get_cats(db: Session):
    return db.query(models.Cat).all()


def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat
