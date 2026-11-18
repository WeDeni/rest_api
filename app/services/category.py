from sqlalchemy.orm import Session
from app.repositories.category import CategoryRepository
from app.schemes.all import Category, CategoryCreate, CategoryUpdate


class CategoryNotFound(Exception):
    '''Категория не найдена'''
    pass

class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[Category]:
        categories_orm = self.category_repository.get_all()
        return [Category.model_validate(category) for category in categories_orm]

    def create_category(self, category_create: CategoryCreate) -> Category:
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return Category.model_validate(category_orm)

    def update_category(self, category_id: str, category_update: CategoryUpdate) -> Category:
        category_for_update = self.category_repository.get_by_id(category_id=category_id)
        if not category_for_update:
            raise CategoryNotFound(f'Категория с id {category_id} не найдена')
        category_for_update.name = category_update.name if category_update.name is not None else category_for_update.name
        self.db.commit()
        return Category.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repository.get_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f'Категория с id {category_id} не найдена')
        self.category_repository.delete(category_for_delete)
        self.db.commit()