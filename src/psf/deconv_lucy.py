#!usr/bin/env python
# -*- coding:utf-8 _*

"""
@File : deconv_lucy.py 
@Author : ljt
@Description: xx
@Time : 2021/6/13 16:48 
"""



import numpy as np
import numpy.random as npr
from scipy.signal import convolve


def richardson_lucy(image, psf, iterations=50, clip=True, filter_epsilon=None):
    """Richardson-Lucy deconvolution.

    Parameters
    ----------
    image : ndarray
       Input degraded image (can be N dimensional).
    psf : ndarray
       The point spread function.
    iterations : int, optional
       Number of iterations. This parameter plays the role of
       regularisation.
    clip : boolean, optional
       True by default. If true, pixel value of the result above 1 or
       under -1 are thresholded for skimage pipeline compatibility.
    filter_epsilon: float, optional
       Value below which intermediate results become 0 to avoid division
       by small numbers.

    Returns
    -------
    im_deconv : ndarray
       The deconvolved image.

    Examples
    --------
    # >>> from skimage import img_as_float, ground_data, restoration
    # >>> camera = img_as_float(ground_data.camera())
    # >>> from scipy.signal import convolve2d
    # >>> psf = np.ones((5, 5)) / 25
    # >>> camera = convolve2d(camera, psf, 'same')
    # >>> camera += 0.1 * camera.std() * np.random.standard_normal(camera.shape)
    # >>> deconvolved = restoration.richardson_lucy(camera, psf, 5)

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Richardson%E2%80%93Lucy_deconvolution
    """
    float_type = np.promote_types(image.dtype, np.float32)
    image = image.astype(float_type, copy=False)
    psf = psf.astype(float_type, copy=False)
    im_deconv = np.full(image.shape, 0.5, dtype=float_type)
    psf_mirror = np.flip(psf)

    for _ in range(iterations):
        conv = convolve(im_deconv, psf, mode='same')
        # image = image + 0.000000001
        conv = np.abs(conv.min()) + 0.0000000001
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
