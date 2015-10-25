from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Float,
    String
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Log(Base):
     __tablename__ = 'logs'
     id = Column(Integer, primary_key=True)
     temperature = Column(Float(2))
     humidity = Column(Float(2))
     wind_speed = Column(Float(2))
     wind_direction = Column(String(10))
     description = Column(String(20))
     rainfall = Column(Float(2))
     sun_up = Column(String(10))
     sun_down = Column(String(10))
     created_date = Column(DateTime, default=datetime.datetime.utcnow)

     def __repr__(self):
         return "%s" % (self.created_date,)


