from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	Id = Column(Integer, primary_key=True)
	Username = Column(String(12, u'utf8mb4_unicode_ci'), nullable=False, unique=True)
	Password = Column(String(128, u'utf8mb4_unicode_ci'), nullable=False)
	LoginKey = Column(String(16, u'utf8mb4_unicode_ci'))
