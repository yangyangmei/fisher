"""
    created by yangyang on 2018/10/1.
"""
from flask import current_app

from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base,db
from sqlalchemy import Column,Integer,String,Float,Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin,current_user  # 为了保存cookie
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish

from app.spider.yushu_book import YuShuBook
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 生成随机token使用

__author__ = "yangyang"

class User(Base,UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    _password = Column("password",String(128))

    # gifts = relationship('Gift')

    @property          # 获取password的值
    def password( self ):
        return self._password

    @password.setter    #为password赋值
    def password( self,raw ):
        self._password = generate_password_hash(raw)

    def check_password( self, raw_password ):
        return check_password_hash(self._password, raw_password)


    def can_save_to_list( self, isbn ):
        if is_isbn_or_key(isbn) != "isbn":
            return False

        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 不允许一个用户同时赠送多本相同的书
        # 一个用户不可能即是赠送者也是索要者

        # 当前用户即不是赠送者也不是索要着，才能进行加入赠送
        gifting = Gift.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first()

        wishing = Wish.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generation_token(self, expration=600):
        s = Serializer(current_app.config["SECRET_KEY"], expration)
        temp = s.dumps({"id":self.id})
        return temp.decode("utf-8")

    @staticmethod
    def reset_password(new_password, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except :
            return False

        uid = data["id"]
        print(uid)
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True


    # 如果不继承mixins，必须写这个方法，如果id不是这个名字，也必须重写这个方法（无论是否继承）
    # def get_id( self ):
    #     return self.id

    def can_send_drift( self, current_gift):
        # 鱼豆必须足够（大于=1），每索取两本书，自己必须送出一本书
        if self.beans < 1:
            return False
        sucess_gifts_count = Gift.query.filter_by(uid=self.id, launched = True).count() # 我送出的礼物数量
        sucess_receive_count = Drift.query.filter_by(requester_id=self.id, pending = PendingStatus.Sucess).count() # 我收到的礼物数量

        return True if sucess_receive_count/2 <= sucess_gifts_count else  False

    @property  #用户的简介信息
    def summary( self ):
        return {
            "nickname":self.nickname,
            "beans":self.beans,
            "email":self.email,
            "send_receive":str(self.send_counter) +"/"+ str(self.receive_counter)
        }

@login_manager.user_loader   # current_user使用
def get_user(uid):
    return User.query.get(uid)