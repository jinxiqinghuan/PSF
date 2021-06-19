#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : mpv2nii.py 
@Author : ljt
@Description: xx
@Time : 2021/6/9 11:57 
"""


import SimpleITK as sitk
import struct
import os
import numpy as np



path = r"D:\ljt\Study\Madic\Project\PSF\data\voxel_11_subset_4.mpv"

# f = open(path, "rb")
size = os.path.getsize(path)

# 此部分只能运行一次，再次运行就会报错 后期设置为保存新文件
with open(path, "rb") as f:
    print(f.__sizeof__())
    tmp = f.read()[16:]
with open(path, "wb") as fw:
    fw.write(tmp)
    fw.close()


arr_data = np.ones((178, 178, 94))


binfile = open(path, 'rb')
size = os.path.getsize(path)
print(size / 4)
for i in range(arr_data.shape[2]):
    for j in range(arr_data.shape[1]):
        for k in range(arr_data.shape[0]):
            data = binfile.read(4)
            data = struct.unpack('f', data)
            # print(i,j,k)
            # print(struct.unpack('f', ground_data))
            arr_data[k,j,i] = data[0]

nii_img = sitk.GetImageFromArray(arr_data)
sitk.WriteImage(nii_img, "test.nii")
print("保存成功！")

