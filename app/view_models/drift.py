"""
    created by yangyang on 2018/10/5.
"""
from app.libs.enums import PendingStatus

__author__ = "yangyang"

class DriftViewModelCollection():
    def __init__(self, drifts, current_user_id):
        self.data = []
        self.__paser(drifts, current_user_id)


    def __paser( self , drifts, current_user_id):
        for drift in drifts:
            self.data.append(DriftViewModel(drift, current_user_id).data)


class DriftViewModel():
    def __init__(self, drift, current_user_id):

        self.data = {}
        self.data = self.__paser(drift, current_user_id)

    @staticmethod
    def requester_or_gifter( drift, current_user_id ):
        """判断是请求者还是接收者"""
        if drift.requester_id == current_user_id:
            you_are = "requester"
        else:
            you_are = "gifter"

        return you_are

    def __paser( self , drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        operator = drift.requester_nickname if you_are !="requester" else  drift.gifter_nickname
        status_str = PendingStatus.pending_str(drift.pending, you_are)
        return {
            "drift_id":drift.id,
            "date":drift.create_datetime.strftime("%Y-%m-%d"),
            "book_img":drift.book_img,
            "book_title":drift.book_title,
            "book_author":drift.book_author,
            "message":drift.message,
            "address":drift.address,
            "recipient_name":drift.recipient_name,
            "mobile":drift.mobile,
            "status":drift.pending,
            "you_are": you_are,
            "operator":operator,
            "status_str":status_str,
        }



