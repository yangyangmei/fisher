"""
    created by yangyang on 2018/9/29.
"""
from flask import  Flask, current_app

__author__ = "yangyang"

app = Flask(__name__)


# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = current_app.config["DEBUG"]
# ctx.pop()

# 实现了上下文协议的对象使用with
# 实现__enter__, __exit__

with app.app_context(): #上下文表达式必须返回一个上下文管理器
    a = current_app
    d = current_app.config["DEBUG"]


class MyResource:
    def __enter__(self):
        print("connection to resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("有异常")
        else:
            print("没有异常")

        print("shi fang zi yuan")

        # return True  # 必须要返回True 或者False, 返回True是不抛出异常，false是抛出异常，如果不返回是抛出异常
        return False

    def query( self ):
        print("查询资源")

try:
    with MyResource() as resource:
        1/0
        resource.query()
except Exception as exc:
    print(exc)

