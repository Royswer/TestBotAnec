from sqlalchemy import Integer, String, Boolean, Date, Text, create_engine, ForeignKey, insert, select, update, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Anecdots(Base):
    __tablename__ = "anecdots"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    text: Mapped[str] = mapped_column(String(2000))
    author: Mapped[int] = mapped_column(Integer, nullable=True)

class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(30))
