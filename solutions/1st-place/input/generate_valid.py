import argparse

import pandas as pd


def get_config():
    ap = argparse.ArgumentParser()

    ap.add_argument('--train', required=True, help="train labels")
    ap.add_argument('--split', type=int, default=6, help="output split number")
    ap.add_argument('--percent', type=float, default=0.02925, help="set percentage to use as validation")

    return ap.parse_args()


def main():
    config = get_config()

    df = pd.read_csv(config.train).set_index('Image')

    df_valid = df.sample(frac=config.percent)
    df_train = df[~df.index.isin(df_valid.index)]

    df_valid.to_csv(f'valid_split_{config.split}.csv')
    df_train.to_csv(f'train_split_{config.split}.csv')


if __name__ == "__main__":
    main()
