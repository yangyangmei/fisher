"""
    created by yangyang on 2018/9/29.
"""
from app.libs.httper import HTTP_Fish
from flask import current_app

__author__ = "yangyang"


class YuShuBook:
    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn( self, isbn ):
        url = self.isbn_url.format(isbn)
        result = HTTP_Fish.get(url)
        print(result)
        self.__fill_single_book(result)

    def search_by_keyword( self, keyword, page=1 ):
        url = self.keyword_url.format(keyword, current_app.config["PER_PAGE"], self.calculate_start(page))
        result = HTTP_Fish.get(url)
        self.__fill_collection_book(result)

    def calculate_start(self, page ):
        return (page - 1) * current_app.config["PER_PAGE"]

    # 双下滑杠代表私有方法
    def __fill_single_book( self ,book):
        if book:
            self.total = 1
            self.books.append(book)
            print(self.books)

    def __fill_collection_book( self,result ):
        self.total = result["total"]
        self.books = result["books"]

    @property   #方便获取第一个元素，获取详情页的时候方便使用，如果没有书，返回None，不会出现out of index
    def first( self ):
        return self.books[0] if self.total>=1 else None


# 下面类的定义是伪类，没有自己的属性特征和行为
# class _YuShuBook:
#     isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
#     keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"
#
#     @classmethod
#     def search_by_isbn(cls, isbn):
#         url = cls.isbn_url.format(isbn)
#         result = HTTP_Fish.get(url)
#         return result
#
#     @classmethod
#     def search_by_keyword( cls,keyword, page=1):
#         url = cls.keyword_url.format(keyword, current_app.config["PER_PAGE"],cls.calculate_start(page))
#         result = HTTP_Fish.get(url)
#         return result
#
#     @staticmethod
#     def calculate_start( page ):
#         return (page-1)*current_app.config["PER_PAGE"]