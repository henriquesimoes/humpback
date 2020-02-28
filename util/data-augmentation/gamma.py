import argparse
import numpy as np
import cv2
import os
from PIL import Image

def do_gamma(image, gamma=1.0):
  table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
  for i in np.arange(0, 256)]).astype("uint8")

  return cv2.LUT(image, table) # apply gamma correction using the lookup table

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", required=False, help="output folder")
ap.add_argument("-i", "--image", required=True, help="path to input image")

args = vars(ap.parse_args())

if not os.path.isfile(args["image"]):
  print("{} not found...".format(args["image"]))
  exit(0)

image = Image.open(args["image"])
original = np.array(image).copy()

image = do_gamma(np.array(image), 1)

print("Not changed? {}".format(np.all(np.equal(image, original))))

image = Image.fromarray(image)
if args["dir"]:
  if not os.path.exists(args["dir"]):
    os.mkdir(args["dir"])
  image.save(os.path.join(args["dir"], os.path.basename(args["image"])))
else:
  image.show()

