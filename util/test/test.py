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

  for name in dfs.keys():
    dfs[name] = dfs[name].sort_index()
  
  assert (dfs['test'].index == dfs['prediction'].index).all()

  dfs['test'] = preprocess.update_new_whales(df_train=dfs['train'], df_test=dfs['test'])

  assert (dfs['test'].index == dfs['prediction'].index).all()

  if config.known_only:
    dfs['test'], dfs['prediction'] = preprocess.remove_new_whales(df_test=dfs['test'], df_pred=dfs['prediction'])

    assert (dfs['test'].index == dfs['prediction'].index).all()

  converter = preprocess.Converter(classes)
  pred, actual = converter.to_numpy(dfs['prediction'], dfs['test'])

  report = ReportManager(config.name)

  report.set_info(solution=config.solution, description=config.description, known_only=config.known_only)

  report.add_metric('MAP@5', metrics.mapk(actual, pred, k=5))

  ks = (1, 3, 5)
  tops = metrics.precisionk(actual, pred, topk=ks)

  for k, top in zip(ks, tops):
    report.add_metric(f'Top@{k}', top)

  report.finish(config.output, save=True)

if __name__ == "__main__":
  main()
