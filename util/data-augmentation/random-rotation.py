import os
import sys

import cv2
import numpy as np
from PIL import Image


def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 {} images_dir".format(__file__))
        exit(0)

    path = sys.argv[1]

    filename = os.path.join(path, "00a3dd76f.jpg")
    image = Image.open(filename)
    image.show()

    image = Image.fromarray(rotate(np.array(image), 20))
    image.show()
