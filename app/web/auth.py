from . import web
from flask import render_template, request, redirect, url_for, flash, current_app
from app.forms.auth import RegisterForm, LoginForm, EmailForm,PasswordForm
from app.models.user import User
from app.models.base import db
from app.models.book import Book
from app.models.gift import Gift  #只有导入数据库中才会有
from app.models.wish import Wish
from flask_login import login_user,logout_user
from app.libs.mail import send_mail

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegisterForm(request.form)
    if request.method == "POST" and registerform.validate():

        with db.auto_commit():
            user = User()
            user.set_attr(registerform.data)
            db.session.add(user)

        return redirect(url_for("web.login"))


    return render_template("auth/register.html", form=registerform)


@web.route('/login', methods=['GET', 'POST'])
def login():
    print("login")
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first() #必须要加.first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True) # 使用第三方flask-login保存cookie ,对应的模型中要进行修改 ,remember=True默认保存365天

            # http://0.0.0.0:5000/login?next=%2Fmy%2Fgifts  从gifts页面跳转后会自动加上一个next参数，如果从/login当前直接进入则没有next值
            next = request.args.get("next")
            if not next or not next.startswith("/"):
                next = url_for("web.index")

            return redirect(next)

            # return redirect(url_for("web.index"))
        else:
            flash("用户名或者邮箱不正确")

    return render_template("auth/login.html", form=form)



@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    email_form = EmailForm(request.form)
    if request.method == "POST":
        if email_form.validate():
            user = User.query.filter_by(email = email_form.email.data).first_or_404() # 使用first_or_404()系统会自己抛出异常
            # if not user:
            #     raise  Exception()
            print(user.nickname)
            send_mail(email_form.email.data, "重置密码",
                      "email/reset_password.html",user=user,
                      token=user.generation_token())
            flash("一封邮件已发送到邮箱" + email_form.email.data + "，请及时查收")


    return render_template('auth/forget_password_request.html',form = email_form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    password_form = PasswordForm(request.form)
    if request.method == "POST" and password_form.validate():
        # 保存到数据库
        # 提示更改密码成功，跳转到首页
        if User.reset_password(password_form.password1.data,token):
            flash("你的密码已更新，请重新登录")
            return redirect(url_for("web.login"))
        else:
            flash("密码重置失败")

    return render_template("auth/forget_password.html", form=password_form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("web.index"))
