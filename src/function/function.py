#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : function.py 
@Author : ljt
@Description: Positron Range
@Time : 2021/5/26 11:17 
"""

import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)

x = np.linspace(0, 2 / 0.005, 101)
# x = -10
# x = 600

y = (0.516 * np.exp(-0.09 * x) + (1 - 0.516) * np.exp(-0.015 * x))
# y = (0.516 * np.exp(-0.379 * x) + (1 - 0.516) * np.exp(-0.031 * x))

plt.plot(x, y, 'r-', lw=3)
plt.show()



def func(x):
    x = x / 0.005
    y1 = (0.516 * np.exp(-0.09 * x) + (1 - 0.516) * np.exp(-0.015 * x))
    return y1


# 验证
tmp = func(1.996)
print(tmp)

"""
0     1
0.5   0.23
1     0.10
1.5   0.05
2     0.02
"""


# 分辨率为0.47时
