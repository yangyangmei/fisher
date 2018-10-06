"""
    created by yangyang on 2018/10/3.
"""
__author__ = "yangyang"

class A():
    def go( self ):
        return object()
    # 加上这个变成函数式A() 可调用对象来调用
    def __call__(self, *args, **kwargs):
        return object()

class B():
    def run( self ):
        return object()

def func():
    return object()

def main(callable):
    # 要在main调用传入的参数，得到一个object对象
    # 不知道callable是什么类型，故需要在对象中加__call__方法，把类变成可通过A()调用
    callable()
