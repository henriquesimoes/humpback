from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
import os

from config import get_config
import metrics
import preprocess
from report import ReportManager

def load_data(config):
  dataset = {}

  dataset['test'] = pd.read_csv(os.path.join(config.test)).set_index('Image')
  dataset['train'] = pd.read_csv(os.path.join(config.train)).set_index('Image')
  dataset['prediction'] = pd.read_csv(config.prediction).set_index('Image')

  classes = pd.read_csv(config.classes)['Id'].unique()  

  return dataset, classes

def main():
  config = get_config()

  dfs, classes = load_data(config)

  dfs['test'] = preprocess.update_new_whales(df_train=dfs['train'], df_test=dfs['test'])

  converter = preprocess.Converter(classes)
  pred, actual = converter.to_numpy(dfs['prediction'], dfs['test'])

  report = ReportManager(config.name)

  report.set_info(solution=config.solution, description=config.description)

  report.add_metric('MAP@5', metrics.mapk(actual, pred, k=5))
  top1, top3, top5 = metrics.precisionk(actual, pred, topk=(1, 3, 5))
  report.add_metric('Top@1', top1)
  report.add_metric('Top@3', top3)
  report.add_metric('Top@5', top5)

  report.finish(config.output)

if __name__ == "__main__":
  main()