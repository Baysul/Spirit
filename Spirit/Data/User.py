# coding: utf-8
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'

    Id = Column(Integer, primary_key=True)
    Username = Column(String(12, u'utf8mb4_unicode_ci'), nullable=False, unique=True)
    Password = Column(String(128, u'utf8mb4_unicode_ci'), nullable=False)
    Swid = Column(String(39, u'utf8mb4_unicode_ci'), nullable=False)
    LoginKey = Column(String(32, u'utf8mb4_unicode_ci'))
    ConfirmationHash = Column(String(128, u'utf8mb4_unicode_ci'))
    Color = Column(Integer, nullable=False, server_default=text("'1'"))
    Head = Column(Integer, nullable=False, server_default=text("'0'"))
    Face = Column(Integer, nullable=False, server_default=text("'0'"))
    Neck = Column(Integer, nullable=False, server_default=text("'0'"))
    Body = Column(Integer, nullable=False, server_default=text("'0'"))
    Hands = Column(Integer, nullable=False, server_default=text("'0'"))
    Feet = Column(Integer, nullable=False, server_default=text("'0'"))
    Photo = Column(Integer, nullable=False, server_default=text("'0'"))
    Pin = Column(Integer, nullable=False, server_default=text("'0'"))