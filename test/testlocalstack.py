"""
    created by yangyang on 2018/9/30.
"""
import time

from werkzeug.local import LocalStack
import threading

__author__ = "yangyang"

s = LocalStack()
s.push(1)
# print(s.top)
# 两个线程有两个栈，互不影响
# LocalStack :线程隔离，栈的特性
def worker():
    print("before new thread data:" + str(s.top))
    s.push(3)

    print("new thread data:" + str(s.top))
    s.pop()
    print("after new thread data:" + str(s.top))

thread1 = threading.Thread(target=worker, name="yangyang")
thread1.start()

time.sleep(1)

print("main thread  "+ str(s.top))



