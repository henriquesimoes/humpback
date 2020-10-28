import argparse
import os
from collections import defaultdict

import pandas as pd


def parse_sizes(file, output):
    file.readline()

    width = []
    height = []
    width_freq = defaultdict(int)
    height_freq = defaultdict(int)
    cnt = []
    for line in file.readlines():
        size, freq = line.strip().split(')')
        size, freq = eval(size + ')'), int(freq)
        w, h = size

        width.append(w)
        height.append(h)
        cnt.append(freq)

        width_freq[w] += freq
        height_freq[h] += freq

    df = pd.DataFrame({'Width': width, 'Height': height, 'Frequency': cnt})
    df.to_csv('{}.{}.csv'.format(output, 'tuple'))

    df = pd.DataFrame({'Width': list(width_freq.keys()), 'Frequency': list(width_freq.values())})
    df.to_csv('{}.{}.csv'.format(output, 'width'))

    df = pd.DataFrame({'Height': list(height_freq.keys()), 'Frequency': list(height_freq.values())})
    df.to_csv('{}.{}.csv'.format(output, 'height'))


def parse_classes(file, output):
    ids = []
    freq = []

    for line in file.readlines():
        cnt, id = [x for x in line.strip().split()]

        ids.append(id)
        freq.append(int(cnt))

    pd.DataFrame({'Id': ids, 'Frequency': freq}).set_index('Id').to_csv('{}.csv'.format(output))


def get_config():
    ap = argparse.ArgumentParser()

    ap.add_argument("--file", type=str, required=True, help="input data file")
    ap.add_argument("--output", type=str, default="output", help="output csv filename")
    ap.add_argument("--type", type=str, default="sizes", choices=["sizes", "classes"],
                    help="Type of the data to be processed")

    return ap.parse_args()


def main():
    config = get_config()

    action = {
        "sizes": parse_sizes,
        "classes": parse_classes,
    }

    if not os.path.exists(config.file):
        print("file {} not found...".format(config.file))
        return

    file = open(config.file, 'r')

    action[config.type](file, output=config.output)


if __name__ == "__main__":
    main()
