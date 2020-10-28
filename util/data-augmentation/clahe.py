import argparse
import os

import cv2
import numpy as np
from PIL import Image


def do_clahe(image, clip=2, grid=16):
    grid = int(grid)

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    gray, a, b = cv2.split(lab)
    gray = cv2.createCLAHE(clipLimit=clip, tileGridSize=(grid, grid)).apply(gray)
    lab = cv2.merge((gray, a, b))
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return image


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-d", "--dir", required=False, help="output folder")

args = vars(ap.parse_args())

if not os.path.isfile(args["image"]):
    print("{} not found...".format(args["image"]))
    exit(0)

image = Image.open(args["image"])
image.show()

image = Image.fromarray(do_clahe(np.array(image).copy()))

if args["dir"]:
    os.makedirs(args["dir"], exist_ok=True)

    image.save(os.path.join(args["dir"], os.path.basename(args["image"])))
else:
    image.show()
