# This is a sample Python script.
import cv2 as cv

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from image_enhancement import *
from image_segmentation import *
from img_recognition import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 图像名称规则
    RootPath = 'imgs//'
    Imgs = []
    for time in range(0, 9):
        Imgs.append(RootPath + str(time) + '.jpg')
    images = cv_read(Imgs)
    enhancement = enhancement(images)
    segmentation = segmentation(enhancement)
    texts = recognition(segmentation)
    for text in texts:
        print(text)


