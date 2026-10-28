from fastapi import FastAPI
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


tasks: list[TaskSchema] = []

book = ''


@app.post('/books')
def create_book(payload: TaskCreateSchema) -> TaskCreateSchema:
    global book
    book = TaskCreateSchema(title=payload.title)
    return book


@app.get('/books')
def read_book():
    return book


@app.post('/tasks')
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task


@app.get('/tasks')
def read_tasks():
    return tasks
