import argparse
import glob
import os

import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from tqdm import tqdm


def contrast(img):
    img = img.convert('RGB')

    pxs = np.asarray(img)

    return pxs.std(axis=(0, 1, 2))


def get_config():
    ap = argparse.ArgumentParser()

    ap.add_argument("--folder", required=True, help="Input image folder")
    ap.add_argument("--plot_output", default="plot.png", help="Output plot filename")
    ap.add_argument("--raw_output", default="raw.csv", help="Raw data filename")

    return ap.parse_args()


def save_raw(filenames, contrasts, output):
    df = pd.DataFrame({'Image': filenames, 'Contrast': contrasts}).set_index('Image')

    df.describe()

    df.to_csv(output)


def main():
    config = get_config()

    x = []
    images = []

    print("Calculating images contrast...")

    for filename in tqdm(glob.glob(config.folder + '/*.*'), ascii=True, desc="Images processed"):
        figure = Image.open(filename)

        images.append(os.path.basename(filename))
        x.append(contrast(figure))

        figure.close()

    print("Saving contrast raw data at {}...".format(config.raw_output))
    save_raw(images, x, config.raw_output)

    print("Making plot... ", end="")

    plt.hist(x, align='mid', rwidth=0.97)
    plt.xlabel('Contrast')
    plt.ylabel('Occurrences')

    print("done.")

    print("Saving plot at {}".format(config.plot_output))

    plt.savefig(config.plot_output, bbox_inches='tight')


if __name__ == '__main__':
    main()
