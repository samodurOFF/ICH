import time

from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine
from sqlalchemy.orm import mapper, registry
from sqlalchemy.orm.session import sessionmaker



# Настройка движка и метаданных
engine = create_engine('sqlite:///example_2.db')
Register = registry() # Base = declarative_base()


# Определение таблицы
user_table = Table('users', Register.metadata,  # Base.metadata
                   Column('id', Integer, primary_key=True),
                   Column('name', String),
                   Column('age', Integer))


# Определение класса
class User:
    pass
    # def __init__(self, name, age):
    #     self.name = name
    #     self.age = age


# Связывание класса с таблицей
Register.map_imperatively(User, user_table)
# Создание таблицы
Register.metadata.create_all(engine)

user = User(name='Karl', age=20)
Session = sessionmaker(bind=engine)

with  Session() as session:
    with session.begin():
        session.add(user)

    # time.sleep(30)

    with session.begin():
        user.age += 5




