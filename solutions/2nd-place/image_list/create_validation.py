import argparse

import pandas as pd


def get_config():
    ap = argparse.ArgumentParser()

    ap.add_argument('--labels', type=str, default='label_list.txt', help='label mapping to integers')
    ap.add_argument('--train', type=str, required=True, help='training set labels')
    ap.add_argument('--test_number', type=int, required=True, help="test number of the output file name")
    ap.add_argument('--percent', type=float, default=0.02365, help="set percentage to use as validation")

    return ap.parse_args()


def main():
    config = get_config()

    df_label = pd.read_csv(config.labels, sep=' ', names=['Id', 'Number']).set_index('Id')
    df = pd.read_csv(config.train).set_index('Image')

    for id, num in df_label.iterrows():
        df.loc[df['Id'] == id, 'Id'] = df_label.loc[id]['Number']

    df_val = df.sample(frac=config.percent)

    print(len(df_val))
    print(len(df_val[df_val['Id'] == -1]) / len(df_val))

    df_val.to_csv(f'test{config.test_number}.val.txt', sep=' ', header=False)
    df.to_csv(f'test{config.test_number}.train.txt', sep=' ', header=False)


if __name__ == "__main__":
    main()
