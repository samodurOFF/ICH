import datetime

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy.sql.sqltypes import DateTime

engine = create_engine('sqlite:///example.db')


class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    description = Column(String(100), nullable=False)
    update_at = Column(DateTime, onupdate=datetime.datetime.now())
