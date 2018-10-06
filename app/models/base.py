"""
    created by yangyang on 2018/10/1.
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy,BaseQuery
from sqlalchemy import SmallInteger, Column, Integer
from contextlib import contextmanager
__author__ = "yangyang"


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit( self ):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    """由于数据库中status=0是记录被删除的数据，重新filter_by方法"""
    def filter_by(self, **kwargs):
        if "status" not in kwargs.keys():
            kwargs["status"] = 1
        return super(Query,self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # __abstract
    __abstract__ = True # 表示这个是基类
    create_time = db.Column(Integer)
    status = Column(SmallInteger, default=1) #是否被删除，1表示存在

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())  #转换成时间戳

    def set_attr( self,attrs_dict ): # 给模型赋值的时候直接调用，要求forms中的字段和models中的字段相同才能加进去
        for key,value in attrs_dict.items():
            if hasattr(self,key) and key != "id":
                print("********************")
                print(key)
                setattr(self,key,value)

    @property
    def create_datetime( self ):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete( self ):
        self.status = 0