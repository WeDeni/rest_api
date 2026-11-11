from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    '''Базовый класс для всех моделей таблиц БД'''
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))