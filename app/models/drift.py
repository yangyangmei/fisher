"""
    created by yangyang on 2018/10/4.
"""
from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base

__author__ = "yangyang"

class Drift(Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'drift'

    # def __init__(self):
    #     self.pending = PendingStatus.waiting
    #     super(Drift, self).__init__()

    # 邮件信息
    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息，记录原始数据
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    _pending = Column("pending",SmallInteger, default=1)
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    @property
    def pending( self ):
        return PendingStatus(self._pending)

    @pending.setter
    def pending( self, status ):
        self._pending = status.value
