from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from contextlib import asynccontextmanager


DATABASE_URL = 'postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres'
engine = create_engine(DATABASE_URL, echo=True)  # объект, который управляет подключениями к базе данных
Sessionlocal = sessionmaker(bind=engine)  # cоздаёт фабрику, из которой можно получать сессии для работы с базой


class Base(DeclarativeBase):
    '''Базовый класс для всех моделей таблиц БД'''
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    '''Модель для таблицы задачи в Базе Данных'''
    __tablename__ = 'tasks'
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False) # по умолчанию False
    
class CategoryORM(Base):
    '''Модель для таблицы категории в Базе Данных'''
    __tablename__ = 'categories'
    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

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
    name: str | None = None

def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()


def task_to_model(task: TaskORM) -> TaskSchema:
    '''Конвертация объекта ORM в Pydantic'''
    return TaskSchema(id=task.id, title=task.title, completed=task.completed)


def category_to_model(category: CategoryORM) -> Category:
    '''Конвертация объекта ORM в Pydantic'''
    return Category(id=category.id, name=category.name)


@app.get('/tasks')
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in tasks_from_db]


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(id=str(uuid4()), title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_to_model(new_task)


@app.patch('/tasks/{task_id}', response_model=TaskSchema)
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    '''
    Обновить существующую задачу
    task_id получаем из url
    payload получаем из тела запроса
    '''
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')

    task.title = payload.title if payload.title is not None else task.title
    task.completed = payload.completed if payload.completed is not None else task.completed
    db.commit()
    return task_to_model(task)


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    '''Удалить задачу'''
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')

    db.delete(task)
    db.commit()


@app.get('/categories')
def read_categories(db: Session = Depends(get_db)) -> list[Category]:
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [category_to_model(category) for category in categories_from_db]


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> Category:
    new_category = CategoryORM(id=str(uuid4()), name=payload.name)
    db.add(new_category)
    db.commit()
    return category_to_model(new_category)


@app.patch('/categories/{category_id}', response_model=Category)
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)) -> Category:
    '''
    Обновить существующую категорию
    category_id получаем из url
    payload получаем из тела запроса
    '''
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')

    category.name = payload.name if payload.name is not None else category.name
    db.commit()
    return category_to_model(category)


@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    '''Удалить категорию'''
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')

    db.delete(category)
    db.commit()
    