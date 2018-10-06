"""
    created by yangyang on 2018/9/30.
"""
import time

from werkzeug.local import Local
import threading

__author__ = "yangyang"


my_obj = Local()
my_obj.b = 1

def worker():
    my_obj.b = 2
    print("i am thread")
    t = threading.current_thread()
    print(t.getName())
    print("in new thread is :"+str(my_obj.b))

new_t = threading.Thread(target=worker, name="haha")
new_t.start()
time.sleep(1)
t = threading.current_thread()
print(t.getName())

print(my_obj.b)