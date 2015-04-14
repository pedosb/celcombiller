"""
Define classes that map the database tables
"""
# pylint: disable=C0103,W0232,R0903
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Sequence,\
        ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

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

    def __repr__(self):
        return '<name=%s clid=%s>' % (self.clid, self.name)


class CDR(Base):
    """
    Call Detail Records holds information about finished calls
    """
    __tablename__ = 'cdr'

    id_ = Column(Integer, Sequence('cdr_id_seq'), primary_key=True)
    answer = Column(DateTime)
    billsec = Column(Integer)
    from_user_id = Column(Integer, ForeignKey('users.id_'))
    from_user = relationship('User', backref='originated_calls',
                             foreign_keys=from_user_id)
    to_user_id = Column(Integer, ForeignKey('users.id_'))
    to_user = relationship('User', backref='received_calls',
                           foreign_keys=to_user_id)

    def __repr__(self):
        return '<from=%s date=%s duration=%s>' % (self.from_user, self.answer,
                                                  self.billsec)

Base.metadata.create_all(engine)
