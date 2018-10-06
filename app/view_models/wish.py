"""
    created by yangyang on 2018/10/3.
"""
from app.view_models.book import BookViewModel

__author__ = "yangyang"

class MyWishViewModels:
    def __init__(self, wishes_of_mine, gifts_count_list):

        self.__wishes_of_mine = wishes_of_mine
        self.__gifts_count_list = gifts_count_list
        self.wishes = self.__parse()

    def __parse( self ):
        temp_gift_list = []
        for wish in self.__wishes_of_mine:
            count = 0
            for gift in self.__gifts_count_list:
                if wish.isbn == gift["isbn"]:
                    count = gift["count"]

            mywish_viewmodel = MyWishViewModel(wish, count)
            temp_gift_list.append(mywish_viewmodel)

        return temp_gift_list



class MyWishViewModel:
    def __init__(self, gift,count):
        self.book = BookViewModel(gift.book)
        self.wishes_count = count
        self.id = gift.id