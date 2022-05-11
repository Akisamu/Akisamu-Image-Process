
import matplotlib.pylab as plt
import cv2 as cv

Imgs = []


def print_add(img) -> None:
    Imgs.append(img)


def print_imgs(name: str) -> None:
    time = 1
    for img in Imgs:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        plt.subplot(3, 3, time)
        plt.imshow(img)
        plt.axis('off')
        plt.title(name + str(time))
        time = time + 1
    plt.show()


def cv_read(paths: list) -> list:
    imgs = []
    for path in paths:
        imgs.append(cv.imread(path))
    return imgs
