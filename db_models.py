from sqlalchemy import Integer, String, Boolean, Date, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Anecdots(Base):
    __tablename__ = "anecdots"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(2000))
    author: Mapped[int] = mapped_column(Integer, nullable=True)

class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(30))

class CategoriesAnecdots(Base):
    __tablename__ = "categories_anecdots"
    id: Mapped[int] = mapped_column(primary_key=True)
    categoryId: Mapped[str] = mapped_column(ForeignKey('categories.id'))
    anecdotId: Mapped[int] = mapped_column(ForeignKey('anecdots.id'))
