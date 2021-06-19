#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : kernel.py
@Author : ljt
@Description: xx
@Time : 2021/6/13 15:10 
"""

import numpy as np

def psf_func(x):
    x = x / 0.005
    y1 = (0.516 * np.exp(-0.09 * x) + (1 - 0.516) * np.exp(-0.015 * x))
    return y1


def build_kernel(k_size, voxel_size):
    half_k = int((k_size - 1) / 2)

    kernel = np.ones((k_size, k_size, k_size))

    for i in range(k_size):
        for j in range(k_size):
            for k in range(k_size):
                dis = np.sqrt(pow((i - half_k), 2) + pow((j - half_k), 2) + pow((k - half_k), 2))
                # func 求处坐标对应的距离
                tmp = psf_func(dis * voxel_size)
                kernel[i][j][k] = tmp

    return kernel / np.sum(kernel)
    # return kernel
