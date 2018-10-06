"""
    created by yangyang on 2018/9/29.
"""

from flask import jsonify, request, render_template, flash
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.trade import TradeViewModel
from . import web
from app.forms.book import SearchForm
from app.view_models.book import BookViewModel, BookCollection
from flask_login import current_user
import json

__author__ = "yangyang"

@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_wishes = False
    has_in_gifts = False

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid = current_user.id,isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid = current_user.id,isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    trade_gifts = Gift.query.filter_by(isbn=isbn,launched=False).all()
    trad_wishes = Wish.query.filter_by(isbn=isbn,launched=False).all()

    trade_gifts_model = TradeViewModel(trade_gifts)
    trade_wishes_model = TradeViewModel(trad_wishes)

    return render_template('book_detail.html',book=book,
                           wishes=trade_wishes_model,gifts=trade_gifts_model,
                           has_in_gifts = has_in_gifts, has_in_wishes=has_in_wishes)

@web.route("/book/search")  # 第三版
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)

        yushu_book = YuShuBook()
        if isbn_or_key == "isbn":
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(q, yushu_book)
        # return json.dumps(books, default= lambda book:book.__dict__)  # json序列化，自定义default函数

    else:
        # return jsonify(form.errors)
        flash("搜索的关键字不符合要求，请重新输入")

    return render_template("search_result.html", books=books)

# @web.route("/book/search")  # 改成？q=jin&page=1的形式  第二版
# def search():
#     form = SearchForm(request.args)
#     if form.validate():
#         q = form.q.data.strip()
#         page = form.page.data
#         isbn_or_key = is_isbn_or_key(q)
#         if isbn_or_key == "isbn":
#             result = YuShuBook.search_by_isbn(q)
#             result = BookViewModel.package_single(result, q)
#         else:
#             result = YuShuBook.search_by_keyword(q, page)
#             result = BookViewModel.package_collection(result, q)
#
#         return jsonify(result)
#
#     else:
#         return jsonify(form.errors)


# @web.route("/book/search/<q>/<page>")  第一版
# def search(q,page):
    # ISBN 13 0-9数字组成
    # ISBN 10个0-9的数字组成，包含一些"-"

    # q = request.args["q"]
    # page = request.args["page"]
    # isbn_or_key = is_isbn_or_key(q)
    # if isbn_or_key == "isbn":
    #     result = YuShuBook.search_by_isbn(q)
    # else:
    #     result = YuShuBook.search_by_keyword(q)
    #
    # # return json. dumps(result) , 200, {"content-type":"application/json"}
    # return jsonify(result)

# @web.route("/test")
# def test():
#     data = {
#         "name":"yy",
#         "age":18
#     }
#     flash("hello flash ", category="error")
#     flash("hello qiyue", category="warning")
#
#
#     return render_template("test.html", data=data)
