#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : utils.py
@Author : ljt
@Description: xx
@Time : 2021/6/18 21:32 
"""


# 次数的norm 只是去掉负值
def norm_img(array):
    if array.min() >= 0:
        print("最小值大于等于0，不norm了")
    else:
        norm_array = array + abs(array.min())
    return norm_array + 0.1
