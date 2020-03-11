import imgaug as ia
from imgaug import augmenters as iaa
import cv2
from PIL import Image
import argparse
import os

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True, help="Image path")

args = vars(ap.parse_args())

imagepath = args["image"]

if not os.path.exists(imagepath):
  print("Not found {}...".format(imagepath))
  exit(1)

image = cv2.imread(imagepath)

seq = iaa.Sequential([
        iaa.Affine(rotate= [0],
                   shear = {'x': 5, 'y': 15},
                   mode='edge')
      ])

image = seq.augment_image(image)

Image.fromarray(image).show()

if input("Save? ") in ["yes", "y", "yep"]:
  cv2.imwrite("shear-" + os.path.basename(imagepath), image)

