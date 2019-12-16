from PIL import Image
from matplotlib import pyplot as plt
import sys, os, glob
from tqdm import tqdm
import numpy as np

def contrast(img):
   pxs = np.asarray(img)

   return pxs.std()

if __name__ == '__main__':
   if len(sys.argv) < 2:
      print("Usage: python3 {} folder [filename]".format(__file__))
      sys.exit(0)

   folder = sys.argv[1]

   if not os.path.isdir(folder):
      print("{} is not a dir...".format(folder))
      sys.exit(1)

   out_filename = sys.argv[2] if len(sys.argv) == 3 else 'plot.png'

   x = []

   print("Calculating images contrast...")

   for filename in tqdm(glob.glob(folder + '/*.*'), ascii=True, desc="Images processed"):
      figure = Image.open(filename)

      x.append(contrast(figure))

      figure.close()

   print("Making plot... ", end="")

   plt.hist(x, align='mid', rwidth=0.97)
   plt.xlabel('Contrast')
   plt.ylabel('Occurrences')

   print("done.")

   print("Saving plot at {}".format(out_filename))

   plt.savefig(out_filename, bbox_inches='tight')
