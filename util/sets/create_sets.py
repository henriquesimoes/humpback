from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import argparse

from processing import *

def get_config():
  ap = argparse.ArgumentParser()

  ap.add_argument("--labels", type=str, required=True, help="set image labels (CSV file)")

  ap.add_argument("--hard", type=str, default=None, help="set hard examples (CSV files comma separated)")
  ap.add_argument("--remove", type=str, dest="not_valid", default=None, help="images not to include in the dataset (CSV file)")
  ap.add_argument("--duplicate-classes", type=str, dest="duplicate_class", default=None, help="duplicate classes to merge")
  ap.add_argument("--duplicate-images", type=str, dest="duplicate_imgs", default=None, help="duplicate images to remove or keep (CSV file)")
  ap.add_argument("--not-new", type=str, dest="not_new", default=None, help="candidate images to be not new with the veridict column (CSV file)")
  ap.add_argument("--mislabeled", type=str, default=None, help="mislabeled images with the correct label (CSV file)")
  ap.add_argument("--new-groups", type=str, default=None, help="images to be assigned with a new id (CSV file)")

  ap.add_argument("--output", type=str, default="sets", help="set output folder")

  return ap.parse_args()

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

  df_standard = hard.apply(df)
  df_hard = df[~df.index.isin(df_standard.index)]

  assert len(df_hard) + len(df_standard) == len(df)

  return df_standard, df_hard

def main():
  config = get_config()

  df, hard_df = get_dataframe(config)

  for 

if __name__ == "__main__":
  main()
