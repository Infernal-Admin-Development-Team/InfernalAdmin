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
    category = Column(Integer)
    poster_id = Column(Integer)
    offender_id = Column(Integer)
    content = Column(String)


class Reference(Base):
    __tablename__ = 'report_reference'
    reference_id = Column(Integer, primary_key=True)
    report_id = ForeignKey(Report.id)
    content = Column(String)
    attachment = Column(String)


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    author_id = Column(Integer)


class Attachment(Base):
    __tablename__ = 'message_attachment'
    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    message_id = ForeignKey(Message.id)
    report = relationship(Report)
    timestamp = Column(DateTime)

class ReportComment(Base):
    __tablename__ = 'report_comment'
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
