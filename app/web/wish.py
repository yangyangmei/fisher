from flask import render_template, redirect, url_for, current_app, flash

from app.libs.mail import send_mail
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.wish import MyWishViewModels
from . import web
from flask_login import login_required, current_user
from app.models.base import db
from app.forms.auth import EmailForm
__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    wishes_of_mine = Wish.get_user_gifts(current_user.id)
    isbn_list = [gift.isbn for gift in wishes_of_mine]
    gifts_count_list = Wish.get_wish_counts(isbn_list)
    wishViewModel = MyWishViewModels(wishes_of_mine, gifts_count_list)
    return render_template("my_wish.html", wishes=wishViewModel.wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            current_user.beans -= current_app.config["BEANS_UPLOAD_ONE_BOOK"]
            db.session.add(wish)

    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))
    # return redirect(url_for("web.my_wish"))



@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.filter_by(id = wid, uid=current_user.id).first_or_404()
    # 查询我是否把它加入到了gift中
    gift = Gift.query.filter_by(uid = current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash("你还没有上次此书，请点击'加入到赠送清单'添加此书，添加前请确保自己可以赠送此书")

    else:
        send_mail(wish.user.email, "有人想送你一本书",
                  "email/satisify_wish.html",wish=wish,
                  gift=gift)
        flash("已向他/她发送了通知，如果同意，你将收到一个鱼漂")
    redirect(url_for("web.book_detail", isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    # 撤销wish清单
    with db.auto_commit():
        wish = Wish.query.filter_by(isbn=isbn, uid = current_user.id).first_or_404()
        wish.delete()
    return redirect(url_for("web.my_wish"))
