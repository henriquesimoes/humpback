import os
import random
import sys

import numpy as np
from PIL import Image


def shift(image):
    width, height, d = image.shape
    zero_image = np.zeros_like(image)
    w = random.randint(0, 20) - 10
    h = random.randint(0, 30) - 15

    zero_image[max(0, w): min(w + width, width), max(h, 0): min(h + height, height)] = \
        image[max(0, -w): min(-w + width, width), max(-h, 0): min(-h + height, height)]

    return zero_image.copy()


def scale(image):
    scale = random.random() * 0.1 + 0.9
    assert 0.9 <= scale <= 1

    width, height, d = image.shape
    zero_image = np.zeros_like(image)

    new_width = round(width * scale)
    new_height = round(height * scale)

    image = np.array(Image.fromarray(image).resize((new_height, new_width)))

    start_w = random.randint(0, width - new_width)
    start_h = random.randint(0, height - new_height)

    zero_image[start_w: start_w + new_width, start_h:start_h + new_height] = image

    return zero_image.copy()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 {} images_dir".format(__file__))
        exit(0)

    path = sys.argv[1]

    filename = os.path.join(path, "00a3dd76f.jpg")
    image = Image.open(filename)
    image.show()

    image = Image.fromarray(shift(np.array(image).copy()))
    image.show()

    image = Image.fromarray(scale(np.array(image).copy()))
    image.show()
