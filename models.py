"""
Define classes that map the database tables
"""
# pylint: disable=W0232,R0903,C0103
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Sequence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:////tmp/celcombiller.db')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    """
    System users each of which has a unique caller id (CLID)
    """
    __tablename__ = 'users'

    id_ = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    clid = Column(String(9), nullable=False, unique=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0)

#Base.metadata.create_all(engine)
