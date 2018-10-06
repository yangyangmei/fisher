"""
    created by yangyang on 2018/9/29.
"""
from sqlalchemy import  Integer, String
from app.models.base import db, Base
from sqlalchemy import Column,Integer,String,Float,Boolean

__author__ = "yangyang"



class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(60), default="未名")
    isbn = Column(String(15), nullable=False, unique=True)
    price = Column(String(20))
    binding = Column(String(20))  # 平装，精装
    pages = Column(Integer)
    summary = Column(String(1000))
    image = Column(String(50))
    publisher = Column(String(50))
    pubdate = Column(String(50))



