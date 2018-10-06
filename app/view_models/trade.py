"""
    created by yangyang on 2018/10/2.
"""
__author__ = "yangyang"
# from flask_login import current_user

class TradeViewModel:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)


    def __parse( self, goods):
        self.total = len(goods)
        self.trades = [self.__parse_single(good) for good in goods]

    def __parse_single( self, good):

        if good.create_datetime:
            create_time = good.create_datetime
        else:
            create_time = "未知"
        return {
            "user_name":good.user.nickname,
            "time":create_time,
            "id":good.id
        }

