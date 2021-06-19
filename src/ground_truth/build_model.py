#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : build_model.py 
@Author : ljt
@Description: xx
@Time : 2021/6/12 10:28 
"""


# 选用 0.709_0.5_0.75VVHR_0.236_211_211_111_60itr_1sub.nii
# 切割部分进行建模
# x: 72-102
# y: 82-130
# z:  47-72

import SimpleITK as sitk
import numpy as np
from numpy.fft import fftn as fftn



# 读取phantom模板原始图像
path = "../../data/ground_data/0.709_0.5_0.75VVHR_0.236_211_211_111_60itr_1sub.nii"
# 读取图片
img = sitk.ReadImage(path)
img_array = sitk.GetArrayFromImage(img)
# 原始SimpleITK数据的存储形式为(Width, Height, Depth)即（X，Y，Z），使用GetArrayFromImage()方法后，X轴与Z轴发生了对调，输出形状为：(Depth, Height, Width)即（Z,Y,X）。

messagesize = img.GetSize()
spacing = img.GetSpacing()
direction = img.GetDirection()
origin = img.GetOrigin()





# x: 72-102
# y: 82-130
# z:  50-72
# 切割
print(img_array.shape) # z轴在前边
new_img_array = img_array[50:72,82:130,72:102]
print(new_img_array.shape)
new_img = sitk.GetImageFromArray(new_img_array)
new_img.SetSpacing(spacing)
print(spacing)
sitk.WriteImage(new_img, "../../data/ground_data/new_img.nii")



model_img_path = "../../data/ground_data/reg.nii.gz"
model_img = sitk.ReadImage(model_img_path)
model_img_array = sitk.GetArrayFromImage(model_img)
model_img = sitk.GetImageFromArray(model_img_array)
model_img.SetSpacing(spacing)
sitk.WriteImage(model_img, "../../data/ground_data/model_img.nii")
model_img_array = sitk.GetArrayFromImage(model_img)


new_img_f = fftn(new_img_array)
model_f = fftn(model_img_array)

H = new_img_f / model_f
print(H.shape)
h1 = np.fft.ifftn(H)
h = np.real(h1)
print(h)
h_img = sitk.GetImageFromArray(h)
sitk.WriteImage(h_img, "../../data/ground_data/h.nii")
h_pad = np.lib.pad(h, ((0,img_array.shape[0] - h.shape[0]), (0, img_array.shape[1] - h.shape[1]), (0, img_array.shape[2] - h.shape[2])), 'constant', constant_values=(0))
print(h_pad)

H = fftn(h_pad)



img_f = fftn(img_array)

recon = img_f / (H + 1)
# print(recon)
recon = np.fft.ifftn(recon)
recon = np.real(recon)
recon_img = sitk.GetImageFromArray(recon)
recon_img.SetSpacing(spacing)
sitk.WriteImage(recon_img, "../../data/ground_data/recon.nii")


