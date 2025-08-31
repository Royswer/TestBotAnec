from sqlalchemy import create_engine, insert, select, func, update
from sqlalchemy.orm import Session
from .db_models import Base, Anecdots, Categories, CategoriesAnecdots


class DB:
    def __init__(self, db_path='database/db.db'):
        self.engine = create_engine(f"sqlite+pysqlite:///{db_path}")
        self.create_db()
        
    def create_db(self):
        Base.metadata.create_all(self.engine)

    # Получить 1 случайный анекдот
    def get_random_anecdot(self):
        with Session(self.engine) as session:
            q = select(Anecdots.text).where(Anecdots.status == 'Одобрено').order_by(func.random()).limit(1)
            result = session.execute(q).first()
            return result[0] if result else "Нет анекдотов"

    # Получить N случайных анекдотов
    def get_random_anecdots(self, count):
        with Session(self.engine) as session:
            q = select(Anecdots.text).where(Anecdots.status == 'Одобрено').order_by(func.random()).limit(count)
            result = session.execute(q).scalars().all()
            return result if result else ["Нет анекдотов"]

    # Получить случайный анекдот из конкретной категории
    def get_random_anecdot_by_category(self, category_id):
        with Session(self.engine) as session:
            q = (
                select(Anecdots.text)
                .join(CategoriesAnecdots, Anecdots.id == CategoriesAnecdots.anecdotId)
                .where(CategoriesAnecdots.categoryId == category_id)
                .order_by(func.random())
                .limit(1)
            )
            result = session.execute(q).first()
            return result[0] if result else "Нет анекдотов в этой категории"

    def add_anec(self, status: str, text: str, user_id: int = None):
        with Session(self.engine) as session:
            q = insert(Anecdots).values(text=text, author=user_id, status=status)
            b = session.execute(q)
            session.commit()
            return b.inserted_primary_key[0] if b.inserted_primary_key else None

    def add_cat(self, category):
        with Session(self.engine) as session:
            q = insert(Categories).values(category=category).prefix_with('OR IGNORE')
            session.execute(q)
            session.commit()
    
    def add_cats(self, category_list: list):
        with Session(self.engine) as session:
            q = insert(Categories).prefix_with('OR IGNORE')
            session.execute(q, category_list)
            session.commit()
    
    def add_cats_anecs(self, categoryId, anecdotId):
        with Session(self.engine) as session:
            q = insert(CategoriesAnecdots).values(categoryId=categoryId, anecdotId=anecdotId)
            session.execute(q)
            session.commit()
    
    def get_id_category(self, category: str) -> int:
        with Session(self.engine) as session:
            q = select(Categories.id).where(Categories.category == category)
            result = session.execute(q).first()
            return result[0] if result else None
    
    def get_id_category_full(self) -> dict:
        with Session(self.engine) as session:
            q = select(Categories.id, Categories.category)
            result = session.execute(q)
            return {row[1]: row[0] for row in result}
        
    def select_categories(self) -> list[dict]:
        with Session(self.engine) as session:
            q = select(Categories.id, Categories.category)
            result = session.execute(q)
            return [{'id': row[0], 'category': row[1]} for row in result]
    
    def my_add_anec_with_categories(self, text, category_names):
        with Session(self.engine) as session:
            # Добавляем анекдот
            new_anek = Anecdots(text=text)
            session.add(new_anek)
            session.flush()  # чтобы получить id до commit

            # Добавляем категории
            for cat_name in category_names:
                category = session.query(Categories).filter_by(category=cat_name).first()
                if not category:
                    category = Categories(category=cat_name)
                    session.add(category)
                    session.flush()
                # Связываем
                link = CategoriesAnecdots(
                    categoryId=category.id,
                    anecdotId=new_anek.id
                )
                session.add(link)
            
            session.commit()
    def update_status_anec(self, anec_id, status):
        q = update(Anecdots).values(status=status).where(Anecdots.id==anec_id)
        with Session(self.engine) as session:
            session.execute(q)
            session.commit()
    



# Тесты
if __name__ == '__main__':
    db_manager = DB('db.db')
    print(db_manager.get_random_anecdots(3))
    print(db_manager.get_random_anecdot_by_category(1))