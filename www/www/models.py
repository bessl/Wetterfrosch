from sqlalchemy import (
    Column,
    Integer,
    DateTime
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


class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    at = Column(DateTime, default=datetime.datetime.now())
    temperature = Column(Integer)
    humidity = Column(Integer)

    def __unicode__(self):
        return u"%s: %sC, %s%%" % (self.at, self.temperature, self.humidity)

