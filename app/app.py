from fastapi import FastAPI
from . import database as db
from .cats.api import router as cats_router

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

app.include_router(prefix="/cats", router=cats_router)
