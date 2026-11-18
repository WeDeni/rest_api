from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class Category(BaseModel):
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate (BaseModel):
    name: str | None = None