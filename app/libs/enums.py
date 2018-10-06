"""
    created by yangyang on 2018/10/4.
"""
__author__ = "yangyang"

from enum import Enum

class PendingStatus(Enum):
    Witing = 1   # 等待
    Sucess = 2
    Reject = 3   # 拒绝
    Redraw = 4   # 撤销

    @classmethod
    def pending_str( cls, status, key ):
        key_map =  {
            cls.Witing:{
                "requester":"等待对方邮寄",
                "gifter":"等待你邮寄"
            },
            cls.Sucess:{
                "requester": "对方已邮寄",
                "gifter": "你已邮寄，交易完成"
            },
            cls.Reject:{
                "requester": "对方已拒绝",
                "gifter": "你已拒绝"
            },
            cls.Redraw:{
                "requester": "你已撤销",
                "gifter": "对方已撤销"
            }
        }

        return key_map[status][key]

