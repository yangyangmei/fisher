"""
    created by yangyang on 2018/10/2.
"""
__author__ = "yangyang"

class MyResource:

    def query( self ):
        print("query data")

from contextlib import contextmanager

# 好处：原来的函数不用修改，可以在外部进行修改调用
@contextmanager  # 把原来不是上下文管理器的类变成了一个上下文管理器
def make_myresource():
    print("connection to resource")

    yield MyResource()

    print("close resource connection")

with make_myresource() as r:
    r.query()


# 栗子 2 灵活使用contextManager
@contextmanager
def book_make():
    print("《", end="")
    yield
    print("》", end="")

with book_make():
    print("且将生活一饮而尽")

