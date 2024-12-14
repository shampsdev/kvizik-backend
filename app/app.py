from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.api import router as core_router
from .core import database as db

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=core_router)
