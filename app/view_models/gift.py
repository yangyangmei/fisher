"""
    created by yangyang on 2018/10/3.
"""
from app.view_models.book import BookViewModel

__author__ = "yangyang"

class MyGiftViewModels:
    def __init__(self, gifts_of_mine, wishes_count_list):

        self.__gifts_of_mine = gifts_of_mine
        self.__wishes_count_list = wishes_count_list
        self.gifts = self.__parse()

    def __parse( self ):
        temp_gift_list = []
        for gift in self.__gifts_of_mine:
            count = 0
            for wish in self.__wishes_count_list:
                if gift.isbn == wish["isbn"]:
                    count = wish["count"]
            print("****************************")
            print(count)
            mygift_viewmodel = MyGiftViewModel(gift, count)
            temp_gift_list.append(mygift_viewmodel)

        return temp_gift_list



class MyGiftViewModel:
    def __init__(self, gift,count):
        self.book = BookViewModel(gift.book)
        self.wishes_count = count
        self.id = gift.id
        # self.user_name = gift.user.nickname
