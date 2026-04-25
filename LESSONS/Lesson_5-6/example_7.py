from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///example_7.db')


class UserTag(Base):
    __tablename__ = 'tags_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    #

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tags = relationship("Tag", secondary='tags_association', backref="users")


Base.metadata.create_all(engine)
