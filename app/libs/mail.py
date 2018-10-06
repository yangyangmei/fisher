"""
    created by yangyang on 2018/10/4.
"""
from threading import Thread

__author__ = "yangyang"
from flask_mail import Message
from flask import current_app, render_template
from app import mail

def send_mail(to, subject, template, **kwargs):
    message = Message("[鱼书]"+subject, sender=current_app.config["MAIL_USERNAME"], recipients=[to])
    print(kwargs)
    message.html = render_template(template,**kwargs)

    # 获取真实的app对象(app=Flask())，不能使用代理的current_app,由于线程隔离的原理，直接传入current_app获取不到栈顶元素
    app = current_app._get_current_object()
    tr = Thread(target=send_async_mail, args=[app, message])
    tr.start()
    # mail.send(message)


def send_async_mail(app,message):
    with app.app_context():
        try:
            mail.send(message)
        except Exception as e:
            # raise e
            pass