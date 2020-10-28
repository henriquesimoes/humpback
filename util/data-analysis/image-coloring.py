import glob
import os
import sys

from PIL import Image
from tqdm import tqdm


def check(image):
    """Returns whether an image is in gray scale"""
    img = image.convert('RGB')

    w, h = img.size

    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            if r != g != b:
                return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 {} folder".format(__file__))
        sys.exit(0)

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        print("{} is not a dir...".format(folder))
        sys.exit(1)

    print("Images processed from: {}".format(folder), end="\n\n")

    gray_scale = 0
    colored = 0

    for imagefile in tqdm(glob.glob(os.path.join(folder, "*.*")), ascii=True, desc='Images processed'):
        image = Image.open(imagefile)

        if check(image):
            gray_scale += 1
        else:
            colored += 1

        image.close()

    total = gray_scale + colored

    print('*** Results ***')
    print('Total images: ', total)
    print('Gray scale: {} ({:.2f}%)'.format(gray_scale, 100 * gray_scale / total))
    print('Colored: {} ({:.2f}%)'.format(colored, 100 * colored / total))
