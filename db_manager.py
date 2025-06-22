from sqlalchemy import create_engine, insert, select, update, delete, func
from sqlalchemy.orm import Session
from db_models import Base, Anecdots, Categories, CategoriesAnecdots


class DB:
    def __init__(self, db_path):
        self.engine = create_engine(f"sqlite+pysqlite:///{db_path}")
    
    def create_db(self):
        Base.metadata.create_all(self.engine)

    def get_random_anecdot(self):
        with Session(self.engine) as session:
            q = select(Anecdots.text).order_by(func.random()).limit(1)
            exec = session.execute(q).first()
            if exec:
                return exec[0]

    def get_random_anecdots(self, count):
        with Session(self.engine) as session:
            q = select(Anecdots.text).order_by(func.random()).limit(count)
            exec = session.execute(q).scalars().all()
            for anec in exec:
                return anec
    
    def add_anec(self, text: str, user_id: int = None):
        with Session(self.engine) as session:
            q = insert(Anecdots).values(text = text, author = user_id)
            session.execute(q)
            session.commit()

    def select_categories(self) -> list[dict]:
        with Session(self.engine) as session:
            q = select(Categories.id, Categories.category)
            result = session.execute(q)
            list_ = []
            for res in result:
                list_.append({
                    'id': res[0],
                    'category': res[1]
                })
            return list_
    
    
#Тесты:
if __name__ == '__main__':
    db_manager = DB('test.db')
    db_manager.create_db()

    test = db_manager.select_categories()
    #print(test)