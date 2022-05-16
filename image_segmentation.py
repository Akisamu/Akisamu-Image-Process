import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from utils import *


def opencv_resize(image, ratio):
    # 重定义图片大小
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv.resize(image, dim, interpolation=cv.INTER_AREA)


def approximate_contour(contour):
    peri = cv.arcLength(contour, True)
    return cv.approxPolyDP(contour, 0.032 * peri, True)


def get_receipt_contour(contours):
    # loop over the contours
    for c in contours:
        approx = approximate_contour(c)

        # if our approximated contour has four points, we can assume it is receipt's rectangle
        if len(approx) == 4:
            return approx


def contour_to_rect(contour, resize_ratio):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # top-left point has the smallest sum
    # bottom-right has the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # compute the difference between the points:
    # the top-right will have the minumum difference
    # the bottom-left will have the maximum difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect / resize_ratio


def wrap_perspective(img, rect):
    # unpack rectangle points: top left, top right, bottom right, bottom left
    (tl, tr, br, bl) = rect

    # compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    # compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # destination points which will be used to map the screen to a "scanned" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # calculate the perspective transform matrix
    M = cv.getPerspectiveTransform(rect, dst)

    # warp the perspective to grab the screen
    return cv.warpPerspective(img, M, (maxWidth, maxHeight))


def segmentation_test(imgs) -> None:

    for img in imgs:

        original = img.copy()

        # resize the picture
        resize_ratio = 500 / img.shape[0]
        imgs_r = opencv_resize(img, resize_ratio)

        # turn to gray
        img = cv.cvtColor(imgs_r, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(img, (5, 5), 0)

        # Canny
        minVal = 50
        maxVal = 100

        edged = cv.Canny(gray, minVal, maxVal)
        plt.imshow(edged)

        contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        largest_contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]
        receipt_contour = get_receipt_contour(largest_contours)

        image_with_receipt_contour = cv.drawContours(imgs_r.copy(), [receipt_contour], -1, (0, 255, 0), 2)

        scanned = wrap_perspective(original.copy(), contour_to_rect(receipt_contour, resize_ratio))

        print_add(gray)
    print_imgs('Cutted')


def segmentation(imgs) -> list:
    ImgList = []
    for img in imgs:
        original = img.copy()

        resize_ratio = 500 / img.shape[0]
        imgs_r = opencv_resize(img, resize_ratio)
        img = cv.cvtColor(imgs_r, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(img, (5, 5), 0)

        minVal = 50
        maxVal = 100
        edged = cv.Canny(gray, minVal, maxVal)

        contours, hierarchy = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        largest_contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]
        receipt_contour = get_receipt_contour(largest_contours)

        scanned = wrap_perspective(original.copy(), contour_to_rect(receipt_contour, resize_ratio))

        ImgList.append(scanned)
    return ImgList
