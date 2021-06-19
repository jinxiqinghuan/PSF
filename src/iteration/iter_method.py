#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : iter_method.py 
@Author : ljt
@Description: xx
@Time : 2021/6/18 21:09 
"""

from src.psf.kernel import *
import SimpleITK as sitk
from scipy import signal


def iter_deconv(path, psf_kernel, iter_num):
    img = sitk.ReadImage(path)
    spacing = img.GetSpacing()
    img_array = sitk.GetArrayFromImage(img)
    print("The shape of input image: ", img_array.shape)
    l = img_array
    print(l.min(), l.max())
    for i in range(iter_num):
        s = signal.fftconvolve(l, psf_kernel, "same")
        s = s + 0.001
        print("s:", s.min(), s.max())
        print("l:", l.min(), l.max())
        g = l / s
        print("g:", g.shape, g.min(), g.max())
        tmp = signal.fftconvolve(g, psf_kernel, "same") + 0.001
        print("tmp:", tmp.shape, tmp.min(), tmp.max())
        l_m = l * tmp
        print("l_m", l_m.shape, l_m.min(), l_m.max())
        out_img = sitk.GetImageFromArray(l_m)
        out_img.SetSpacing(spacing)
        sitk.WriteImage(out_img, "../../output/iter_method_{}.nii".format(i))
        l = l_m



if __name__ == '__main__':
    path = r"D:\ljt\Study\Madic\Project\PSF\data\phantom_0.561_0.38_0.48_VHR_0.28.nii"
    kernel = build_kernel(15, 1)
    iter_deconv(path, kernel, iter_num=10)
