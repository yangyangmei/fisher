"""
    created by yangyang on 2018/9/30.
"""
__author__ = "yangyang"


import threading


def worker():
    print("i am thread")
    t = threading.current_thread()
    print(t.getName())

new_t = threading.Thread(target=worker, name="haha")
new_t.start()

t = threading.current_thread()
print(t.getName())




