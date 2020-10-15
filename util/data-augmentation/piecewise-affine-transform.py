import argparse
import os

import numpy as np
from PIL import Image
from imgaug import augmenters as iaa

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Input image path")
ap.add_argument("-g", "--grid", type=int, default=4, help="grid size")
ap.add_argument("-r", "--range", required=True, help="Percentage range to limit transformation")
ap.add_argument("-d", "--folder", default="output", required=False, help="Output folder")

config = ap.parse_args()

config.range = tuple(map(float, config.range.split(',')))

imagefile = config.image

if not os.path.exists(imagefile):
    print("Not found {}...".format(imagefile))
    exit(1)

original = Image.open(imagefile)
original = np.array(original)[48:481, :]
original = np.array(Image.fromarray(original).resize((512, 256)))
image = original.copy()

seq = iaa.Sequential([
    iaa.PiecewiseAffine(scale=config.range, nb_cols=config.grid, nb_rows=config.grid)
])

image = seq.augment_image(image)
Image.fromarray(original).show()
Image.fromarray(image).show()

if input("Save? ").lower() in ["yes", "y", "yep"]:
    id = input("Enter the identifier: ").lower().split()[0]
    folder = config.folder

    os.makedirs(folder, exist_ok=True)

    Image.fromarray(image).save(os.path.join(folder, id + os.path.basename(imagefile)))
