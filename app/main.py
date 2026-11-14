from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session
from contextlib import asynccontextmanager



from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router

#
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:8080'],
    allow_methods=['*'],
)

'''
class CategoryORM(Base):
    __tablename__ = 'categories'
    name: Mapped[str]


class Category(BaseModel):
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate (BaseModel):
    name: str | None = None


def category_to_model(category: CategoryORM) -> Category:
    return Category(id=category.id, name=category.name)


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
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')

    category.name = payload.name if payload.name is not None else category.name
    db.commit()
    return category_to_model(category)


@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')

    db.delete(category)
    db.commit()
'''