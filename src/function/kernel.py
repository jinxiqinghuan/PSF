#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : kernel.py 
@Author : ljt
@Description: xx
@Time : 2021/6/1 12:35 
"""

import numpy as np
from function import func

kernel = np.ones((5, 5, 5))
# print(kernel[3][3][3])
num = []

"""
0     1
0.5   0.23
1     0.10
1.5   0.05
2     0.02
"""

for i in range(8):
    for j in range(8):
        for k in range(8):
            dis = np.sqrt(pow((i-2), 2) + pow((j-2), 2) + pow((k-2), 2))
            tmp = func(dis)
            kernel[i][j][k] = tmp

print(kernel)

            # if dis == 0:
            #     kernel[i][j][k] = 1
            # elif dis == 1:
            #     kernel[i][j][k] = 0.23
            # elif dis == 2:
            #     kernel[i][j][k] = 0.10
            # elif dis == 3:
            #     kernel[i][j][k] = 0.05


# print(np.sum(kernel))
# print(kernel)

# num = list(set(num))
# print(num)

# for i in kernel:
#     for j in i:
#         for k in j:
#             tmp = (i - 3)#(i - 3)  + (j - 3)(j - 3) + (k - 3)(k - 3)
#             print(tmp)


                # kernel[i][j][k]