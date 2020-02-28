import numpy as np
from PIL import Image
import os, sys

def do_brightness_shift(image, alpha=0.125):
  image = image.astype(np.float32)
  image = image + alpha*255
  image = np.clip(image, 0, 255).astype(np.uint8)
  return image


def do_brightness_multiply(image, alpha=1):
  image = image.astype(np.float32)
  image = alpha*image
  image = np.clip(image, 0, 255).astype(np.uint8)
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
  original = image = Image.open(filename)
  image.show()

  image = Image.fromarray(do_brightness_multiply(np.array(image)))
  #image.save(os.path.join(output, "mult-" + os.path.basename(filename)))
  #image.show()
