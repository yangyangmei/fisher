"""
    created by yangyang on 2018/9/29.
"""
__author__ = "yangyang"

def is_isbn_or_key(word):
    """判断是否是isbn"""
    isbn_or_key = "key"
    if len(word) == 13 and word.isdigit():
        isbn_or_key = "isbn"
    short_word = word.replace("-", "")
    if "-" in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = "isbn"

    return isbn_or_key
