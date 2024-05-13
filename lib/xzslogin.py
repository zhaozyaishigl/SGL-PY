# ！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         :2024/4/17 16:32
# Author        : smart
# @File         :xzslogin.py
# @Software     :PyCharm
import unittest,requests


class xzs():
    def xzslogin(self, a, b):
        url = "http://127.0.0.1:8000/api/user/login"
        heard = {
                'Content-Type':'application/json'
               }
        data = {"userName": a, "password": b, "remember": False}
        r = requests.post(url=url, headers=heard, json=data)
        # print(r.text)
        return r.text

if __name__ == '__main__':
    unittest.main()
    # b=xzs()
    # b.xzslogin('admin', '123456')
    # b.xzslogin('', '123456')