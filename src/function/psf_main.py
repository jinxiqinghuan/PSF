#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : psf_main.py
@Author : ljt
@Description: xx
@Time : 2021/6/1 8:56 
"""

import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
from function import func
from numpy.fft import fftn as fftn
# from scipy.fft import fftn as fftn
from scipy.signal import deconvolve as decv
from skimage import color, data, restoration
# restoration.richardson_lucy()
from src.psf.kernel import *

path = "../../data/0.561_VVHR_0.187_0.5_0.75.nii"

# PSF恢复kernel

voxel_size = 0.561
kernel_size = 7
half_k_size = int((kernel_size - 1) / 2)

kernel = build_kernel(kernel_size, voxel_size)

pos = 10

# 读取图片
sitkImage = sitk.ReadImage(path)
img = sitk.GetArrayFromImage(sitk.ReadImage(path))
messagesize = sitkImage.GetSize()
spacing = sitkImage.GetSpacing()
direction = sitkImage.GetDirection()
origin = sitkImage.GetOrigin()
print(spacing)
# print(messagesize, spacing, direction, origin)


# img = np.lib.pad(img, ((0, ll), (0, ll), (0, ll)), 'constant', constant_values=(0))
img_f = fftn(img)

# kernel傅里叶变换
kernel_pad = np.lib.pad(kernel, (
(0, img_f.shape[0] - kernel_size), (0, img_f.shape[1] - kernel_size), (0, img_f.shape[1] - kernel_size)), 'constant',
                        constant_values=(0))
# print(kernel_pad.shape)

# kernel_pad.shape
kernel_img = sitk.GetImageFromArray(kernel_pad)
kernel_pad_f = fftn(kernel_pad)
# kernel_pad_fshift = np.fft.fftshift(kernel_pad_f)
# kernel_pad_pin = 20 * np.log(np.abs(kernel_pad_f))


# PSF矫正
# recon = img_f / (kernel_pad_f + 0.000001)

# img_f += np.abs(img_f.min()) + 0.00001
# kernel_pad_f += np.abs(kernel_pad_f.min() + 0.00001)
recon = img_f / (kernel_pad_f + 0.01)

recon = np.fft.ifftn(recon)
recon = np.real(recon)
recon = recon[:-half_k_size, :-half_k_size, :-half_k_size]

recon = np.lib.pad(recon, ((half_k_size, 0), (half_k_size, 0), (half_k_size, 0)), 'constant', constant_values=(0))

print(recon.shape)

# save
# output = sitk.GetImageFromArray(recon)
# numpy ground_data to sitk
sitk_image = sitk.GetImageFromArray(recon)

# print(sitk_image.GetSize(), sitk_image.GetSpacing(), sitk_image.GetDirection(), sitk_image.GetOrigin())
# sitk_image.SetOrigin(origin)
sitk_image.SetSpacing(spacing)
# sitk_image.SetDirection(direction)
print(sitk_image.GetSize(), sitk_image.GetSpacing(), sitk_image.GetDirection(), sitk_image.GetOrigin())

sitk.WriteImage(sitk_image, "../../output/ff_output.nii")
# sitk.WriteImage(kernel_img, "../ground_data/kernel{0}.nii".format(ll))
print("PSF处理并保存成功！")
