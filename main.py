from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:8080'],
    allow_methods=['*'],
)

class TaskSchema(BaseModel):
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
    name: str


tasks: list[TaskSchema] = []
categories: list[Category] = []


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task


@app.get('/tasks')
def read_tasks():
    return tasks


@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
        return task


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
        return


# # #
# # #
# # #


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate) -> Category:
    new_category = Category(id=str(uuid4()), name=payload.name)
    categories.append(new_category)
    return new_category


@app.get('/categories')
def read_categories():
    return categories


@app.patch('/categories/{category_id}')
def update_category(category_id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name
            return category


@app.delete('/categories/{category_id}')
def delete_category(category_id):
    found = False
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            found = True
    if found:
        return status.HTTP_204_NO_CONTENT
    else:
        return status.HTTP_404_NOT_FOUND