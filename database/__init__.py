from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from util import CONFIG

print("starting db")
Base = declarative_base()


class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True)
    poster_id = Column(Integer)


class ReportComment(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    report_id = ForeignKey(Report.id)
    report = relationship(Report)
    content = Column(String)
    timestamp = Column(DateTime)
    visible_to_reporter = Column(Boolean)


engine = create_engine(CONFIG.db.endpoint)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
