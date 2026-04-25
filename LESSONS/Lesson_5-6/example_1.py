from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import logging

engine = create_engine('sqlite:///example.db')

# Настройка базового логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname) | %(name)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

# Включение логирования SQL-запросов
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class Base(DeclarativeBase):
    pass


# Определяем класс `User`, который наследуется от базового класса `Base`.
# Этот класс представляет собой сущность базы данных.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    age = Column(Integer)


# Для того чтобы в базе данных появилась таблицы вызываем метод `create_all()` объекта `metadata` базового класса `Base`
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
with Session() as session:
    with session.begin():
        new_user = User(name="John Doe", age=30)
        session.add(new_user)

print(new_user)
print(session.is_active)
