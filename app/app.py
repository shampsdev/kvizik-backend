from fastapi import FastAPI

from .cats.api import router as cats_router
from .db import database as db

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

app.include_router(prefix="/cats", router=cats_router)
