# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, text
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
    Avatar = Column(Integer, nullable=False)
    AvatarAttributes = Column(String(98, u'utf8mb4_unicode_ci'), nullable=False,server_default=text(
	    """'{"spriteScale":100,"spriteSpeed":100,"ignoresBlockLayer":false,"invisible":false,"floating":false}'"""))
    Coins = Column(Integer, nullable=False, server_default=text("'10000'"))
    Moderator = Column(Boolean, nullable=False, default=False)
    Color = Column(Integer, nullable=False, server_default=text("'1'"))
    Head = Column(Integer, nullable=False, server_default=text("'0'"))
    Face = Column(Integer, nullable=False, server_default=text("'0'"))
    Neck = Column(Integer, nullable=False, server_default=text("'0'"))
    Body = Column(Integer, nullable=False, server_default=text("'0'"))
    Hands = Column(Integer, nullable=False, server_default=text("'0'"))
    Feet = Column(Integer, nullable=False, server_default=text("'0'"))
    Photo = Column(Integer, nullable=False, server_default=text("'0'"))
    Pin = Column(Integer, nullable=False, server_default=text("'0'"))
