from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from util import CONFIG

Base = declarative_base()


class Report(Base):
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    status = Column(Integer)  # 0->Open 1->IN_PROGRESS 2->Resolved 3->Rejected
    poster_id = Column(Integer)
    offender_id = Column(Integer)
    content = Column(String)

class Message(Base):
    """Same as discord message"""
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    author = Column(Integer)
    content = Column(String)
    timestamp = Column(DateTime)


class Attachment(Base):
    """Attachment used for a message"""
    __tablename__ = 'message_attachment'
    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    message_id = ForeignKey(Message.id)
    message = relationship(Message)


class Reference(Base):
    """Messages the user copies from the server to use as evidence"""
    __tablename__ = 'report_reference'
    id = Column(Integer, primary_key=True)
    message_id = ForeignKey(Message.id)
    report_id = ForeignKey(Report.id)
    message = relationship(Message)
    report = relationship(Report)


class ReportContent(Base):
    """Messages the user copies from the server to use as evidence"""
    __tablename__ = 'report_content'
    id = Column(Integer, primary_key=True)
    message_id = ForeignKey(Message.id)
    report_id = ForeignKey(Report.id)
    message = relationship(Message)
    report = relationship(Report)


class ReportComment(Base):
    """Comments admins and the poster use to follow up on reports"""
    __tablename__ = 'report_comment'
    id = Column(Integer, primary_key=True)
    message_id = ForeignKey(Message.id)
    report_id = ForeignKey(Report.id)
    message = relationship(Message)
    report = relationship(Report)
    visible_to_poster = Column(Boolean)


engine = create_engine(CONFIG.db.endpoint)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
