from sqlalchemy import select
from app.models.all import CategoryORM

# GET, CREATE, DELETE
class CategoryRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id: str) -> CategoryORM:
        return self.db.get(CategoryORM, category_id)

    def create(self, name:str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete(self, category:CategoryORM) -> None:
        self.db.delete(category)