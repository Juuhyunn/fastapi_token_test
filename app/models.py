from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(String(200), nullable=False)
  password = Column(String(200), nullable=False)
