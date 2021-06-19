#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : old_main.py
@Author : ljt
@Description: xx
@Time : 2021/6/13 11:46 
"""

import numpy as np
import SimpleITK as sitk
from scipy.signal import convolve
from skimage.restoration import deconvolution

voxel_size = 0.236


def psf_func(x):
    x = x / 0.005
    y1 = (0.516 * np.exp(-0.09 * x) + (1 - 0.516) * np.exp(-0.015 * x))
    return y1


def build_kernel(k_size):
    half_k = int((k_size - 1) / 2)

    kernel = np.ones((k_size, k_size, k_size))
    num = []

    for i in range(k_size):
        for j in range(k_size):
            for k in range(k_size):
                dis = np.sqrt(pow((i - half_k), 2) + pow((j - half_k), 2) + pow((k - half_k), 2))
                # func 求处坐标对应的距离
                tmp = psf_func(dis * voxel_size)
                kernel[i][j][k] = tmp
    return kernel


def deconv(img, kernel, iteration, clip=False, filter_epsilon=None):

    float_type = np.promote_types(img.dtype, np.float32)
    image = img.astype(float_type, copy=False)
    psf = kernel.astype(float_type, copy=False)
    im_deconv = np.full(image.shape, 0.5, dtype=float_type)
    psf_mirror = np.flip(psf)

    for _ in range(iteration):
        conv = convolve(im_deconv, psf, mode='same')
        # image = image + 0.000000001
        conv = conv.min() + 0.0000000001
        # if filter_epsilon:
        # filter_epsilon = conv.min() + 0.00000001
        if filter_epsilon:
            relative_blur = np.where(conv < filter_epsilon, 0, image / conv)
        else:
            relative_blur = image / conv
        im_deconv *= convolve(relative_blur, psf_mirror, mode='same')

    if clip:
        im_deconv[im_deconv > 1] = 1
        im_deconv[im_deconv < -1] = -1

    return im_deconv


if __name__ == '__main__':
    # 输入图片路径
    path = "../../data/0.709_0.5_0.75VVHR_0.236_211_211_111_60itr_1sub.nii"
    kernel = build_kernel(17)
    img = sitk.GetArrayFromImage(sitk.ReadImage(path))
    output = deconv(img, kernel, iteration=1)
    print(kernel.shape)
    sitk.WriteImage(sitk.GetImageFromArray(output), "tmp.nii")
    sitk.WriteImage(sitk.GetImageFromArray(kernel), "kernel.nii")

