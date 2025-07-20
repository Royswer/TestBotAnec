from sqlalchemy import create_engine, insert, select, update, delete, func
from sqlalchemy.orm import Session
from db_models import Base, Anecdots, Categories, CategoriesAnecdots


class DB:
    def __init__(self, db_path = 'db.db'):
        self.engine = create_engine(f"sqlite+pysqlite:///{db_path}")
        self.create_db()
        
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
            b = session.execute(q)
            session.commit()
            
            if b.inserted_primary_key:
                inserted_id = b.inserted_primary_key[0]
                return inserted_id
    
    def add_cat(self, category):
        with Session(self.engine) as session:
            q = insert(Categories).values(category = category).prefix_with('OR IGNORE')
            session.execute(q)
            session.commit()
    
    def add_cats(self, category: list):
        with Session(self.engine) as session:
            q = insert(Categories).prefix_with('OR IGNORE')
            session.execute(q, category)
            session.commit()
    
    def add_cats_anecs(self, categoryId, anecdotId):
        with Session(self.engine) as session:
            q = insert(CategoriesAnecdots).values(categoryId = categoryId, anecdotId = anecdotId)
            session.execute(q)
            session.commit()
    
    def get_id_category(self, category: str) -> int:
         with Session(self.engine) as session:
            q = select(Categories.id).where(Categories.category == category)
            result = session.execute(q).first()
            if result:
                return result[0]
            return None
    
    def get_id_category_full(self) -> int:
         with Session(self.engine) as session:
            q = select(Categories.id, Categories.category)
            result = session.execute(q)
            #for cat in result:
                #print(cat)
            categ = {}
            for i in result:
                categ[i[1]] = i[0]
            return categ
        
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
    
    def my_add_anec_with_categories(self, text, category_names):
        with Session(self.engine) as session:
            new_anek = Anecdots(text=text)
            session.add(new_anek)
            session.commit()
        for cat_name in category_names:
            category = session.query(Categories).filter_by(category=cat_name).first()
            if not category:
                category = Categories(category=cat_name)
                session.add(category)
                session.commit()

        link = CategoriesAnecdots(
            categoryId=category.id,
            anecdotId=new_anek.id
        )
        session.add(link)
        session.commit()
    
#Тесты:
if __name__ == '__main__':
    db_manager = DB('db.db')
    res = db_manager.get_id_category_full()
    print(res)
    