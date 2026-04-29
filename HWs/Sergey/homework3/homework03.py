'''Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.'''
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine('sqlite:///:memory:')

'''Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.'''
Session = sessionmaker(bind=engine)
session = Session()

'''Задача 3: Определите модель продукта Product со следующими типами колонок:
id: числовой идентификатор
name: строка (макс. 100 символов)
price: числовое значение с фиксированной точностью
in_stock: логическое значение'''

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(DECIMAL(7,2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

'''Задача 4: Определите связанную модель категории Category со следующими типами колонок:
id: числовой идентификатор
name: строка (макс. 100 символов)
description: строка (макс. 255 символов)'''
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    product = relationship("Product", backref="category")

'''Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.'''
# line 27 and 38
