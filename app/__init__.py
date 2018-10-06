"""
    created by yangyang on 2018/9/29.
"""
from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

__author__ = "yangyang"

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.secure")
    app.config.from_object("app.setting")
    register_blueprint(app)

    mail.init_app(app)
    login_manager.init_app(app)  # 初始化loginManager
    login_manager.login_view = "web.login"  # 加上后没有授权的页面会转入到这个页面
    login_manager.login_message = "请先登录或注册"  #默认的是英文的提示

    db.init_app(app)  # 初始化
    # with app.app_context():  # 或者使用这种方式，需要查看create_all()里面深层定义查看 人为push了app_context
    #     # db.drop_all()
    #     db.create_all()
    db.create_all(app=app)  # 生成数据表, 这种方式在当前代码环境中最容易实现


    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)

