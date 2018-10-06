"""
    created by yangyang on 2018/9/29.
"""
__author__ = "yangyang"

import requests


class HTTP_Fish:

    @staticmethod
    def get(url, return_json=True ):
        r = requests.get(url)

        # 使用三元表达式简化代码
        if r.status_code != 200:
            return {} if return_json else ""

        return r.json() if return_json else r.text


        # if r.status_code == 200:
        #     if return_json:
        #         return r.json()
        #     else:
        #         return r.text
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ""
