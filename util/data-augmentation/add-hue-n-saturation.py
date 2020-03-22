import imgaug as ia
from imgaug import augmenters as iaa
import os
from PIL import Image
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Input image path")

args = vars(ap.parse_args())

imagefile = args["image"]

if not os.path.exists(imagefile):
  print("Not found {}...".format(imagefile))
  exit(1)


original = Image.open(imagefile)
original = np.array(original)
image = np.array(original)

seq = iaa.Sequential([
  iaa.AddToHueAndSaturation((5,5))
])

image = seq.augment_image(image)
Image.fromarray(original).show()
Image.fromarray(image).show()