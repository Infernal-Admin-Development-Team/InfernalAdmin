from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, DateTime, Boolean
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
    poster_id = Column(BigInteger)
    offender_id = Column(BigInteger)
    content = Column(String)
    timestamp = Column(DateTime)
    offending_Messages = relationship("Reference")
    comments = relationship("ReportComment")
    channel = Column(BigInteger)


class Message(Base):
    """Same as discord message"""
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    channel = Column(BigInteger)
    author = Column(BigInteger)
    content = Column(String)
    timestamp = Column(DateTime)
    attachments = relationship("Attachment")


class Attachment(Base):
    """Attachment used for a message"""
    __tablename__ = 'message_attachment'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('message.id'))
    file_link = Column(String)
    file_path = Column(String)
    is_local = Column(Boolean)

    #message = relationship(Message)


class Reference(Base):
    """Messages the user copies from the server to use as evidence"""
    __tablename__ = 'report_reference'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('message.id'))
    report_id = Column(Integer, ForeignKey('report.id'))



class ReportComment(Base):
    """Comments admins and the poster use to follow up on reports"""
    __tablename__ = 'report_comment'
    id = Column(Integer, primary_key=True)

    message_id = Column(Integer, ForeignKey('message.id'))

    report_id = Column(Integer, ForeignKey('report.id'))
    visible_to_poster = Column(Boolean)



engine = create_engine(CONFIG.db.endpoint)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


def clear_db():
    """Destroys the database."""
    with engine.connect() as con:
        con.execute("DROP TABLE report_comment;")

        con.execute("DROP TABLE report_reference;")
        con.execute("DROP TABLE message_attachment;")
        con.execute("DROP TABLE message;")
        con.execute("DROP TABLE report;")
