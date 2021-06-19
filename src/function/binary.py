#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : binary.py 
@Author : ljt
@Description: xx
@Time : 2021/6/8 9:28 
"""

import SimpleITK as sitk
import struct
import os
import numpy as np
import matplotlib.pyplot as plt


path = r"D:\ljt\Study\Madic\0.943_0.5-0.75_Phantom\0.709_202008031434_0.5_0.75mm_Phantom_FDG94uci_vertical_time1800s_TOR2.35_Sigma1_TOR核7_60itr_1sub\VVHR_0.236_211_211_111_60itr_1sub\voxel_59_subset_0.mpv"

# f = open(path, "rb")
size = os.path.getsize(path)
# 此部分只能运行一次，再次运行就会报错 后期保存新文件
# with open(path, "rb") as f:
#     print(f.__sizeof__())
#     tmp = f.read()[16:]
# with open(path, "wb") as fw:
#     fw.write(tmp)
#     fw.close()


arr_data = np.ones((211, 211, 111))


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

path = "test.nii"
sitkImage = sitk.ReadImage(path)
img = sitk.GetArrayFromImage(sitk.ReadImage(path))
plt.imshow(img[:,100, :], "gray")
plt.show()



# show dicom series image
messagesize = sitkImage.GetSize()
spacing = sitkImage.GetSpacing()
direction = sitkImage.GetDirection()
origin = sitkImage.GetOrigin()

print(messagesize, spacing, direction, origin)

# if __name__ == '__main__':
#     filepath='../ground_data/voxel_11_subset_4.mpv'
#     binfile = open(filepath, 'rb') #打开二进制文件
#     size = os.path.getsize(filepath) #获得文件大小
#     # # for i in range(size):
#     # #     ground_data = binfile.read(1) #每次输出一个字节
#     # #     print(ground_data)
#     for i in range(16):
#         ground_data = binfile.read(4)
#         num = struct.unpack('f', ground_data)
#         print(num[0])
#     # print(binfile)
#
#     binfile.close()
