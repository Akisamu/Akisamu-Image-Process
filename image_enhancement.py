# https://pypi.org/project/opencv-python/
import cv2 as cv

# https://numpy.org/
import numpy as np

# https://matplotlib.org/
import matplotlib.pylab as plt

from utils import *


def enhancement_test(imgs: list) -> None:

    time = 1
    ImgList = []

    for img in imgs:

        # 均值模糊 ,去椒盐噪声
        res1 = cv.blur(img, (5, 5))
        # 方框滤波
        res2 = cv.boxFilter(res1, -1, (5, 5), normalize=1)
        # 高斯滤波，
        res3 = cv.GaussianBlur(res2, (3, 3), 0)

        print_add(res3)
    print_imgs('enhancement')


def enhancement(imgs: list) -> list:
    time = 1
    ImgList = []

    for img in imgs:
        res = cv.GaussianBlur(cv.boxFilter(cv.blur(img, (5, 5)), -1, (5, 5), normalize=1), (3, 3), 0)
        ImgList.append(res)
    return ImgList



