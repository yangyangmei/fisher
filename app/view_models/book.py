"""
    created by yangyang on 2018/9/30.
"""
__author__ = "yangyang"


class BookViewModel:
    def __init__(self, book):
        self.title = book["title"]
        self.publisher = book["publisher"]
        self.summary = book["summary"] or ""
        self.price = book["price"]
        self.isbn = book["isbn"]
        self.pages = book["pages"] or ""
        self.author = "、".join(book["author"])
        self.image = book["image"]
        self.pubdate = book["pubdate"]
        self.binding = book["binding"]

    @property    # 函数加上这个属性后变成属性
    def intro( self ):
        intros = filter(lambda x:True if x else False,
                        [self.author,self.publisher,self.price])

        return "/".join(intros)



class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ""

    def fill( self, keyword, yushu_book ):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]

# 以下类定义不合格，上面代码进行了重构
# class _BookViewModel:
#     @classmethod
#     def package_single( cls, data,keyword ):
#         resulted = {
#             "books": [],
#             "total": 0,
#             "keyword": keyword
#         }
#         if data:
#             resulted["total"] = "1"
#             resulted["books"] = [cls.__cut_single_book(data)]
#
#         return resulted
#
#     @classmethod
#     def package_collection( cls, data, keyword ):
#         resulted = {
#             "books": [],
#             "total": 0,
#             "keyword": keyword
#         }
#         if data:
#             resulted["total"] = data["total"]
#             resulted["books"] = [cls.__cut_single_book(book) for book in data["books"]]
#
#         return resulted
#
#     @classmethod
#     def __cut_single_book( self, data ):
#         return {
#             "title":data["title"],
#             "publisher":data["publisher"],
#             "summary":data["summary"] or "",
#             "price": data["price"],
#             "pages":data["pages"] or "",
#             "author": "、".join(data["author"]),
#             "image": data["image"]
#         }
