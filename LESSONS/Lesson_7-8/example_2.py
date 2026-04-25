from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from sqlalchemy import desc

Base = declarative_base()
engine = create_engine('sqlite:///example_2.db')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Numeric)
    created_at = Column(DateTime)
    user = relationship("User", back_populates="orders")

# Base.metadata.create_all(engine)



# Добавление пользователей
# user1 = User(name="Alice", age=30)
# user2 = User(name="Bob", age=22)
# session.add_all([user1, user2])
# session.commit()
#
# # Добавление заказов
# order1 = Order(user_id=user1.id, amount=100.50, created_at=datetime.now() - timedelta(days=1))
# order2 = Order(user_id=user1.id, amount=200.75, created_at=datetime.now())
# order3 = Order(user_id=user2.id, amount=80.99, created_at=datetime.now() - timedelta(days=2))
# session.add_all([order1, order2, order3])
# session.commit()



# Подзапрос для определения последнего заказа каждого пользователя
subquery = session.query(
    Order.user_id,
    func.max(Order.created_at).label('last_order_time')
).group_by(Order.user_id).subquery()

# Основной запрос, который присоединяет пользователей, их заказы и подзапрос последних заказов
complex_query = session.query(
    User.name,
    User.age,
    func.round(Order.amount, 2),
    subquery.c.last_order_time
).join(
    # User.orders
    Order
).join(
    subquery, User.id == subquery.c.user_id
).filter(
    Order.created_at == subquery.c.last_order_time
).order_by(User.name, desc(Order.amount))

# Вывод результатов
for result in complex_query.all():
    print(result)

# ('Alice', 30, 200.75, datetime.datetime(2026, 4, 23, 14, 39, 41, 900732))
# ('Bob', 22, 80.99, datetime.datetime(2026, 4, 21, 14, 39, 41, 901186))