import datetime

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import ForeignKey

from sqlalchemy.sql.sqltypes import DateTime

engine = create_engine('sqlite:///example_5.db')
Base = declarative_base()

class User(Base):
   __tablename__ = 'user'
   id = Column(Integer, primary_key=True)
   name = Column(String)
   age = Column(Integer)
   address = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    street = Column(String, nullable=False)
    user = relationship("User", back_populates="address")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user1 = User(name="John Doe", age=30)
user2 = User(name="Alice Smith", age=25)

address1 = Address(street="123 Main St", user=user1)
address2 = Address(street="456 Elm St", user=user1)
address3 = Address(street="789 Oak St", user=user2)

session.add(user1)
session.add(user2)
session.add(address1)
session.add(address2)
session.add(address3)

session.commit()

print(*[address.street for address in user1.address], sep='\n')
print(address3.user.name)
session.close()
