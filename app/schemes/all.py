from pydantic import BaseModel, ConfigDict, StringConstraints
from typing import Annotated


NonBlankString = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    completed: bool

class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: NonBlankString

class CategoryUpdate(BaseModel):
    name: NonBlankString | None = None

class TaskCreateSchema(BaseModel):
    title: NonBlankString

class TaskUpdateSchema(BaseModel):
    title: NonBlankString | None = None
    completed: bool | None = None