from fastapi import FastAPI

from .core.api import router as core_router
from .core import database as db

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

app.include_router(router=core_router)
