from sqlalchemy import create_engine, insert, select, update, delete, func
from sqlalchemy.orm import Session
from db_models import Base, Anecdots, Categories

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

    
    # def add_users(self, users: list[dict]):
    #     with Session(self.engine) as session:
    #         q = insert(User).prefix_with('OR IGNORE')
    #         session.execute(q, users)
    #         session.commit()

    
    
#Тесты:
if __name__ == '__main__':
    db_manager = DB('test.db')
    db_manager.create_db()

    test = db_manager.get_random_anecdot()
    print(test)