import re

import cv2 as cv
import numpy as np
from skimage.filters import threshold_local
from PIL import Image
import pytesseract
from utils import *


def bw_scanner(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    T = threshold_local(gray, 35, offset = 5, method = "gaussian")
    return (gray > T).astype("uint8") * 255


def recognition_test(imgs: list) -> None:
    time = 1
    pytesseract.pytesseract.tesseract_cmd = r'W:\Program Files\Tesseract-OCR\tesseract.exe'
    for img in imgs:
        result = bw_scanner(img)
        print_add(result)
        pytesseract.pytesseract.tesseract_cmd = r'W:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(result)
        # re.findall(r'\d{18}', text)[0]
        print(str(time) + ' : ' + re.findall(r'\d{18}', text)[0])
        time = time + 1
    print_imgs('final')


def recognition(imgs: list) -> list:
    NumList = []
    pytesseract.pytesseract.tesseract_cmd = r'W:\Program Files\Tesseract-OCR\tesseract.exe'
    for img in imgs:
        result = bw_scanner(img)
        pytesseract.pytesseract.tesseract_cmd = r'W:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(result)
        NumList.append(re.findall(r'\d{18}', text)[0])
    return NumList


