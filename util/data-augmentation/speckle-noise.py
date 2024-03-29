import os
import sys

import cv2
import numpy as np
from PIL import Image


def standard(image, sigma=0.5):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    gray, a, b = cv2.split(lab)
    gray = gray.astype(np.float32) / 255
    H, W = gray.shape

    noise = sigma * np.random.randn(H, W)
    noisy = gray * noise

    noisy = (np.clip(noisy, 0, 1) * 255).astype(np.uint8)
    lab = cv2.merge((noisy, a, b))
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return image


def earhian(image, sigma=0.5):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    gray, a, b = cv2.split(lab)
    gray = gray.astype(np.float32) / 255
    H, W = gray.shape

    noise = sigma * np.random.randn(H, W)
    noisy = gray + gray * noise

    noisy = (np.clip(noisy, 0, 1) * 255).astype(np.uint8)
    lab = cv2.merge((noisy, a, b))
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return image


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 {} images_dir output_dir".format(__file__))
        exit(0)

    path = sys.argv[1]
    output = sys.argv[2]

    if not os.path.exists(output):
        os.mkdir(output)

    filename = os.path.join(path, "00a3dd76f.jpg")
    image = Image.open(filename)
    image.show()

    image = Image.fromarray(standard(np.array(image)))
    image.save(os.path.join(output, "std-speckle-" + os.path.basename(filename)))
    image.show()
