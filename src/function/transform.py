#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : transform.py 
@Author : ljt
@Description: 转换NII文件的spacing
@Time : 2021/6/10 11:45 
"""

import SimpleITK as sitk


path1 = "../../ground_data/voxel_24_subset_0.nii"
path2 = "../../ground_data/voxel_24_subset_0.nii"

img1 = sitk.ReadImage(path1)
img2 = sitk.ReadImage(path2)

# 原始SimpleITK数据的存储形式为(Width, Height, Depth)即（X，Y，Z）
# 使用GetArrayFromImage()方法后，X轴与Z轴发生了对调
# 输出形状为：(Depth, Height, Width)即（Z,Y,X）。
img_array = sitk.GetArrayFromImage(img1)


# show dicom series image
# 图像在各维度的像素个数
messagesize = img1.GetSize()
# 体素大小
spacing = img1.GetSpacing()
# 新坐标系在原坐标系上各个方向的投影
direction = img1.GetDirection()
# 图像原点的坐标（物理层面的，有单位，一般为mm，与spacing保持一致）
origin = img1.GetOrigin()

print(messagesize, spacing, direction, origin)

# # 将img2设置与img1相同的spacing
# img2.SetSpacing(spacing)
# sitk.WriteImage(img2, "../../output/trans_tmp.nii")
