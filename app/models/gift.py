"""
    created by yangyang on 2018/10/1.
"""
from flask import current_app

from app.models.base import Base,db
from sqlalchemy import Column, Integer, String, Boolean, desc,func
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook

__author__ = "yangyang"

class Gift(Base):
    __tablename__ = "gift"
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)  # 表示礼物是否已经送出去,False表示添加到了赠送清单还没有赠送，True表示已经赠送过
    uid = Column(Integer, db.ForeignKey("user.id"))

    user = relationship("User")

    isbn = Column(String(15), nullable=False)

    # book  = db.relationship("Book")
    # bid = db.Column(Integer, db.ForeignKey("book.id"))  # 此案例没有保存书的数据

    @property
    def book( self ):
        # 根据当前的isbn获取这本书
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 首页：显示最近书籍，最近的礼物，！，只显示一定数量（30）
    # 按照时间倒序排序，最新的排在前面
    # 去重，同一本书籍的礼物不重复 （用分组）
    # 链式调用---主体是Query,下面的子函数返回的都是query主体,触发语句：first(),all() 最终生成sql语句去数据库中触发查询
    @classmethod  #对象代表一个礼物，具体。类代表礼物这个事物，它是抽象，不是具体的"一个"
    def recent( cls ):
        # rencent_gift = Gift.query.filter_by(
        #     launched=False).group_by(
        #     Gift.isbn).order_by(
        #     Gift.create_time).limit(5).distinct().all()

        # 课程讲的distinct 要配合group_by使用
        rencent_gift = Gift.query.filter_by(
            launched=False).order_by(Gift.create_time.desc()).limit(
            current_app.config["RENCENT_BOOK_COUNT"]).distinct(Gift.isbn).all()
        # rencent_gift = Gift.query.filter_by(
        #     launched=False).group_by(Gift.isbn).order_by(Gift.create_time.desc()).limit(
        #     current_app.config["RENCENT_BOOK_COUNT"]).all()

        print(len(rencent_gift))

        # print (db.session.query(db.distinct(Gift.isbn)).all())

        return rencent_gift

    @classmethod  #获取我的所有想赠送的礼物
    def get_user_gifts( cls, uid ):
        return Gift.query.filter_by(
            uid = uid, launched=False).order_by(
            Gift.create_time.desc()).all()

    @classmethod  # filter中要使用表达式
    def get_wish_counts( cls, isbn_list):
        # 根据传入的一组isbn,到wish表中检索出相应的礼物，并计算出某个礼物的wish心愿数量
        from app.models.wish import Wish
        wishes = db.session.query(Wish.isbn,func.count(Wish.id)).filter(
            Wish.launched==False, Wish.status==1, Wish.isbn.in_(isbn_list)).group_by(Wish.isbn).all()

        count_list = [{"count":w[1],"isbn":w[0]} for w in wishes]
        return count_list


    def send_drift_by_myself( self, uid ):
        return True if self.user.id == uid else False

