'''Задача 1: Наполнение данными
Добавьте в базу данных следующие категории и продукты'''
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean, Text, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    price = Column(DECIMAL(7,2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(Text)
    products = relationship("Product", backref="category")


Base.metadata.create_all(engine)

'''Добавление категорий: Добавьте в таблицу categories следующие категории:
Название: "Электроника", Описание: "Гаджеты и устройства."
Название: "Книги", Описание: "Печатные книги и электронные книги."
Название: "Одежда", Описание: "Одежда для мужчин и женщин."'''
category_1 = Category(name="Электроника", description="Гаджеты и устройства.")
category_2 = Category(name="Книги", description="Печатные книги и электронные книги.")
category_3 = Category(name="Одежда", description="Одежда для мужчин и женщин.")

session.add_all([category_1, category_2, category_3])
session.commit()

'''Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с
соответствующей категорией:
Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда'''
product_1 = Product(name="Смартфон", price=299.99, in_stock=True, category_id=1)
product_2 = Product(name="Ноутбук", price=499.99, in_stock=True, category_id=1)
product_3 = Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=2)
product_4 = Product(name="Джинсы", price=40.50, in_stock=True, category_id=3)
product_5 = Product(name="Футболка", price=20.00, in_stock=True, category_id=3)

session.add_all([product_1, product_2, product_3, product_4, product_5])
session.commit()

'''Задача 2: Чтение данных
Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, 
включая их названия и цены.'''
query_category = session.query(Category).all()
for category in query_category:
    print(f"{category.id}. {category.name} - {category.description}:")
    for product in category.products:
        print(f" *** Название: {product.name}, Цена: {product.price}, Наличие: {product.in_stock}")
    print("-" * 70)

'''Задача 3: Обновление данных
Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.'''
product = session.query(Product).filter(Product.name == "Смартфон").first()
product.price = 349.99
session.commit()
print("-" * 70)
print(f" *** Название: {product.name}, Цена: {product.price}, Наличие: {product.in_stock}")

'''Задача 4: Агрегация и группировка
Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.'''
total_prod_in_ctg = (session.query(Category.name, func.count(Product.id).label('count_products')).outerjoin(Product
                    ).group_by(Category.id).order_by(Category.id).all())
print("-" * 70)
for item in total_prod_in_ctg:
    print("-" * 70)
    print(f"Категория: '{item[0]}' - Количество: {item[1]}")
print("-" * 70)

'''Задача 5: Группировка с фильтрацией
Отфильтруйте и выведите только те категории, в которых более одного продукта.'''
print("-" * 70)
ctg_with_mult_prod = (session.query(Category.name, func.count(Product.id).label('count_products')).outerjoin(Product
                    ).group_by(Category.id).having(func.count(Product.id) > 1).all())
print("Категории с более чем 1 продуктом:")
for item in ctg_with_mult_prod:
    print(item[0])
