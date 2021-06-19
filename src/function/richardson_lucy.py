#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : richardson_lucy.py
@Author : ljt
@Description: xx
@Time : 2021/6/11 12:39 
"""

#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : psf_main.py
@Author : ljt
@Description: xx
@Time : 2021/6/1 8:56 
"""
import SimpleITK as sitk
from skimage.restoration import richardson_lucy
from src.psf.kernel import build_kernel
from src.psf.deconv_lucy import richardson_lucy

# PSF恢复kernel
voxel_size = 1
kernel_size = 3


if __name__ == '__main__':
    path = "../../data/0.561_VVHR_0.187_0.5_0.75.nii"
    kernel = build_kernel(k_size=kernel_size, voxel_size=voxel_size)
    sitkImage = sitk.ReadImage(path)
    img = sitk.GetArrayFromImage(sitk.ReadImage(path))
    # show dicom series image
    spacing = sitkImage.GetSpacing()
    print(spacing)
    for i in range(0, 10):
        iterations = i + 1
        output = richardson_lucy(img, kernel, clip=True, iterations=iterations)
        output_img = sitk.GetImageFromArray(output)
        output_img.SetSpacing(spacing)
        sitk.WriteImage(output_img, "../../output/iter{}.nii".format(iterations))
        print("第{}次iteration的迭代结果已保存!".format(iterations))
    print("所有迭代完成")
