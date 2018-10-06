"""
    created by yangyang on 2018/10/2.
"""
from app.models.base import Base,db
from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook

__author__ = "yangyang"

class Wish(Base):
    __tablename__ = "wish"
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)  # 表示礼物是否收到,False表示添加到了心愿清单还没有收到，True表示已经收到
    uid = Column(Integer, db.ForeignKey("user.id"))

    user = relationship("User")

    isbn = Column(String(15), nullable=False)

    @property
    def book( self ):
        # 根据当前的isbn获取这本书
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod  # 获取我的所有想要的礼物
    def get_user_gifts( cls, uid ):
        return Wish.query.filter_by(
            uid=uid, launched=False).order_by(
            Wish.create_time.desc()).all()


    @classmethod
    def get_wish_counts( cls, isbn_list ):
        # 根据传入的一组isbn,到Gift表中检索出要赠送的人，并计算出某个礼物可以赠送的Gift数量
        from app.models.gift import Gift
        gifts = db.session.query(Gift.isbn, func.count(Gift.id)).filter(
            Gift.launched == False, Gift.status == 1, Gift.isbn.in_(isbn_list)).group_by(Gift.isbn).all()

        count_list = [{"count": w[1], "isbn": w[0]} for w in gifts]
        return count_list


