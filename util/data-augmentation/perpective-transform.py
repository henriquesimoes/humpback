import imgaug as ia
from imgaug import augmenters as iaa
import os
from PIL import Image
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Input image path")
ap.add_argument("-o", "--output", required=False, default="prspt-transf", help="Output folder")

args = vars(ap.parse_args())

imagefile = args["image"]

if not os.path.exists(imagefile):
  print("Not found {}...".format(imagefile))
  exit(1)


original = Image.open(imagefile)
original = np.array(original)[48:481, :]
original = np.array(Image.fromarray(original).resize((512, 256)))
image = original.copy()

seq = iaa.Sequential([
  iaa.PerspectiveTransform(scale=(0.15, 0.15), keep_size=False)
])

image = seq.augment_image(image)
Image.fromarray(original).show()
Image.fromarray(image).show()

if input("Save? ") in ["yes", "y", "yep"]:
  os.makedirs(args["output"], exist_ok=True)

  id = ""
  if input("Identifier (yes/no)? ") in ["yes", "y", "yep"]:
    id = input("\tEnter id: ")

  outname = os.path.join(args["output"], id + os.path.basename(imagefile))

  print("Saving at {}".format(outname))
  Image.fromarray(image).save(outname)

  print("Done...")
  