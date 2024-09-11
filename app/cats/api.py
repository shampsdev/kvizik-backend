from fastapi import APIRouter, Depends, HTTPException
from . import crud, schemas
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def get_cats(db: Session = Depends(get_db)):
    return crud.get_cats(db)


@router.get("/{cat_id}")
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    db_cat = crud.get_cat(db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat


@router.post("/", response_model=schemas.Cat)
def create_cat(cat: schemas.CatCreate, db: Session = Depends(get_db)):
    return crud.create_cat(db=db, cat=cat)
