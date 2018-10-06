
from flask import render_template, request, flash, redirect, url_for

from app.forms.book import DriftForm
from app.libs.enums import PendingStatus
from app.libs.mail import send_mail
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from flask_login import login_required,current_user

from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftViewModelCollection
from . import web
from sqlalchemy import or_

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if  current_gift.send_drift_by_myself(current_user.id):
        flash("这本书是你自己的，不能向自己索要书籍")
    can =  current_user.can_send_drift(current_gift)
    if not can:
        return render_template("not_enough_beans.html",beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == "POST" and form.validate():
        save_drift(form, current_gift)
        # 短信通知
        send_mail(current_gift.user.email, "有人想要一本书",
                  "email/get_gift.html", wisher=current_user,
                  gift=current_gift)


    gifter = current_gift.user.summary
    return render_template("drift.html",gifter=gifter, user_beans= current_user.beans, form=form)




@web.route('/pending')
@login_required
def pending():
    """交易记录"""
    drifts = Drift.query.filter(or_(current_user.id == Drift.requester_id,
                                  current_user.id == Drift.gifter_id)).order_by(Drift.create_time.desc()).all()
    driftsdata = DriftViewModelCollection(drifts, current_user.id).data
    return render_template("pending.html",drifts = driftsdata)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    # 书籍的拥有者才能进行拒绝操作
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id= current_user.id ,id = did).first_or_404()
        drift.pending = PendingStatus.Reject

        # db.session.add(drift)
        current_user.beans += 1 # 撤销后鱼豆要+1

    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    # 撤销操作：书籍的索要着才能执行，为了防止超权，判断当前用户的id和drift里面的请求者id相同
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id= current_user.id ,id = did).first_or_404()
        drift.pending = PendingStatus.Redraw

        # db.session.add(drift)
        current_user.beans += 1 # 撤销后鱼豆要+1

    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    # 发送成功，礼物拥有者发送成功
    # drift中状态改变，wish，gift中launched 改成True
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id= current_user.id ,id = did).first_or_404()
        drift.pending = PendingStatus.Sucess

        # wish_id = drift.


        gift = Gift.query.filter_by(id=drift.gift_id, launched=False).first_or_404()
        gift.launched = True

        # 请求者，心愿达成,和上面是一样的，两种写法
        Wish.query.filter_by(uid = drift.requester_id, launched=False,isbn=drift.isbn).update({Wish.launched:False})

    return redirect(url_for("web.pending"))

def save_drift(drift_form, current_gift):
    # 保存到drift, 用户鱼豆-1
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)  # 把drift_form中的元素都添加到drift对应的属性中，名字需相同

        book = BookViewModel(current_gift.book)
        drift.isbn = book.isbn
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image

        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname

        drift.gifter_id = current_gift.user.id
        drift.gift_id = current_gift.id
        drift.gifter_nickname = current_gift.user.nickname
        # drift.pending = PendingStatus.Witing  # pending默认是1，不用再进行赋值

        current_user.beans -= 1

        db.session.add(drift)




