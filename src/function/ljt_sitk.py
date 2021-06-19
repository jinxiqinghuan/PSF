#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : ljt_sitk.py 
@Author : ljt
@Description: 自定义函数库
@Time : 2021/5/25 16:51 
"""
import math

import SimpleITK as sitk
import numpy as np
from sklearn import preprocessing


"""
描述： 读取nii格式影像
返回： Array
"""
def nii_read(path):
    return sitk.GetArrayFromImage(sitk.ReadImage(path))


"""
描述： 对输入影像进行简单归一化
"""
def nii_norm(img):
    if img.min() > 0:
        img = img - img.min()
        norm_img = img / img.max()
    elif img.min() <= 0:
        img = img + math.fabs(img.min())
        norm_img = img / img.max()

    print("归一化结果: ", norm_img.min(), norm_img.max())
    return norm_img

"""
Z-score标准化
"""
def get_average(records):
    return sum(records) / len(records)
def get_variance(records):
    average = get_average(records)
    return sum([(x - average) ** 2 for x in records]) / len(records)
def get_standard_deviation(records):
    variance = get_variance(records)
    return math.sqrt(variance)
def get_z_score(records):
    avg = get_average(records)
    stan = get_standard_deviation(records)
    scores = [(i-avg)/stan for i in records]
    return scores


def z_score(data):
    return preprocessing.scale(data)



"""
描述：dcm2nii
参数：path     dcm序列的地址
     name     保存的文件的地址和文件名
"""
def dcm2nii(path, name):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(path)
    reader.SetFileNames(dicom_names)
    image2 = reader.Execute()
    # image_array = sitk.GetArrayFromImage(image2)  # z, y, x
    # origin = image2.GetOrigin()  # x, y, z
    # spacing = image2.GetSpacing()  # x, y, z
    # image3 = sitk.GetImageFromArray(image2)  ##其他三维数据修改原本的数据，
    sitk.WriteImage(image2, name)  # 这里可以直接换成image2 这样就保存了原来的数据成了nii格式了。
































