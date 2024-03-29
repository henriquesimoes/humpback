from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import pandas as pd
from processing import *


def get_config():
    ap = argparse.ArgumentParser()

    ap.add_argument("--labels", type=str, required=True, help="set image labels (CSV file)")

    ap.add_argument("--hard", type=str, default=None, help="set hard examples (CSV files comma separated)")
    ap.add_argument("--remove", type=str, dest="not_valid", default=None,
                    help="images not to include in the dataset (CSV file)")
    ap.add_argument("--duplicate-classes", type=str, dest="duplicate_class", default=None,
                    help="duplicate classes to merge")
    ap.add_argument("--duplicate-images", type=str, dest="duplicate_imgs", default=None,
                    help="duplicate images to remove or keep (CSV file)")
    ap.add_argument("--not-new", type=str, dest="not_new", default=None,
                    help="candidate images to be not new with the veridict column (CSV file)")
    ap.add_argument("--mislabeled", type=str, default=None, help="mislabeled images with the correct label (CSV file)")
    ap.add_argument("--new-groups", type=str, default=None, help="images to be assigned with a new id (CSV file)")

    ap.add_argument("--tests", type=int, default=5, help="set total number of tests to be created")
    ap.add_argument("--test_percentage", type=float, dest="test_p", default=.2, help="set test dataset proportion")

    ap.add_argument("--output", type=str, default="sets", help="set output folder")

    return ap.parse_args()


def stats(df, start='\t', end='\n'):
    print(f'{start}classes:', len(df[df['Id'] != 'new_whale']['Id'].unique()))
    print(f'{start}known whales:', len(df[df['Id'] != 'new_whale']))
    print(f'{start}new whales:', len(df[df['Id'] == 'new_whale']), end=end)


def get_dataframe(config):
    df = pd.read_csv(config.labels).set_index('Image')
    hard_filters = config.hard.split(',') if config.hard else []

    correct_label = LabelProcessing(mislabeled=config.mislabeled, not_new=config.not_new)
    duplicate = DuplicateProcessing(images=config.duplicate_imgs, classes=config.duplicate_class)
    ignore = IgnoreProcessing(files=[config.not_valid])
    hard = IgnoreProcessing(files=hard_filters)

    df = correct_label.apply(df)
    df = duplicate.apply(df)
    df = ignore.apply(df)

    print('number of classes:', len(df[df['Id'] != 'new_whale']['Id'].unique()))

    df_standard = hard.apply(df)
    df_hard = df[~df.index.isin(df_standard.index)]

    assert len(df_hard) + len(df_standard) == len(df)

    print('standard examples:', len(df_standard))
    stats(df_standard)
    print('hard examples:', len(df_hard))
    stats(df_hard)
    print('total examples:', len(df))
    stats(df)

    return df_standard, df_hard


def main():
    config = get_config()

    df, df_hard = get_dataframe(config)

    builder = DatasetBuilder(df_standard=df, df_hard=df_hard, test_percentage=config.test_p)

    outdir = os.path.join(config.output, "test#{}")

    df_hard.to_csv(os.path.join(config.output, "hard.csv"))

    for i in range(config.tests):
        folder = outdir.format(i + 1)
        df_train, df_test = builder.build()

        print(f'Stats test #{i + 1}:')
        print(f'\ttrain dataset: {len(df_train)} ({len(df_train) / (len(df_train) + len(df_test))})')
        stats(df_train, start='\t\t')

        print(f'\ttest dataset: {len(df_test)} ({len(df_test) / (len(df_train) + len(df_test))})')
        stats(df_test, start='\t\t', end='\n\n')

        os.makedirs(folder, exist_ok=True)
        df_train.to_csv(os.path.join(folder, "train.csv"))
        df_test.to_csv(os.path.join(folder, "test.csv"))

    print('{} tests created on `{}` folder...'.format(config.tests, config.output))


if __name__ == "__main__":
    main()
