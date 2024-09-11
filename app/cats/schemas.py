from pydantic import BaseModel


class CatCreate(BaseModel):
    name: str
    is_fat: bool | None = None


class Cat(BaseModel):
    id: int
    name: str
    is_fat: bool

    class Config:
        from_attributes = True
