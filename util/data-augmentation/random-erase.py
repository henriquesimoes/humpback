import argparse
import os
import random
import sys

import numpy as np
from PIL import Image


def earhian(image):
    if (len(image.shape) != 3):
        return image

    width, height, d = image.shape
    x = random.randint(0, width)
    y = random.randint(0, height)
    b_w = random.randint(5, 10)
    b_h = random.randint(5, 10)

    image[x:x + b_w, y:y + b_h] = 0

    return image


def random_valued(image):
    if (len(image.shape) != 3):
        return image

    width, height, d = image.shape
    x = random.randint(0, width - 100)
    y = random.randint(0, height - 100)
    delta_x = random.randint(50, 100)
    delta_y = random.randint(50, 100)

    image[x: x + delta_x, y: y + delta_y, :] = [
        [[random.randint(0, 255) for ___ in range(0, 3)] for _ in range(0, delta_y)] for __ in range(0, delta_x)]

    return image


def mean_valued(image):
    if (len(image.shape) != 3):
        return image

    width, height, d = image.shape
    x = random.randint(0, width - 100)
    y = random.randint(0, height - 100)
    delta_x = random.randint(50, 100)
    delta_y = random.randint(50, 100)

    image[x: x + delta_x, y: y + delta_y, :] = np.mean(image)

    return image


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--imagedir", required=False, default="../../data/train")
    ap.add_argument("-o", "--output", required=False, default="{}-result".format(sys.argv[0][:-3]))

    args = vars(ap.parse_args())

    path = args["imagedir"]
    output = args["output"]

    os.makedirs(output, exist_ok=True)

    filename = os.path.join(path, "00a3dd76f.jpg")
    x0, y0, x1, y1 = (32, 104, 1048, 464)

    print("Opening image {}".format(filename))
    image = Image.open(filename)
    image_np = np.array(Image.fromarray(np.array(image)[y0:y1, x0:x1]).resize((512, 256)))

    image = Image.fromarray(earhian(image_np.copy()))
    image.save(os.path.join(output, 'earhian-' + os.path.basename(filename)))

    image = Image.fromarray(random_valued(image_np.copy()))
    image.save(os.path.join(output, 'random-' + os.path.basename(filename)))

    image = Image.fromarray(mean_valued(image_np.copy()))
    image.save(os.path.join(output, "mean-" + os.path.basename(filename)))
