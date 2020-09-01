from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import numpy as np

def update_new_whales(df_train, df_test):
  '''
  Updates the known labels to `new_whale` label when necessary.

  It is necessary to do so when the identifiable whale has not been
  seen by the network during its training time. Thus, the better it
  can do is to classify it as a new whale. 

  # Parameters
  
  df_train : `pandas.DataFrame`, required
    Training dataset with Image and Id columns, indexed on Image
  df_test : `pandas.DataFrame`, required
    Test dataset with Image and Id columns, indexed on Image

  # Returns
  
  df_test : `pandas.DataFrame`
    Updated test dataset
  '''

  test_classes = df_test['Id'].unique()
  train_classes = df_train['Id'].unique()

  disjoint = test_classes[~np.isin(test_classes, train_classes)]

  for id in disjoint:
    df_test.loc[df_test['Id'] == id] = 'new_whale'

  return df_test

def remove_new_whales(df_test, df_pred):
  nw_indices = df_test.loc[df_test['Id'] == 'new_whale'].index

  df_test = df_test.loc[~df_test.index.isin(nw_indices)].copy()
  df_pred = df_pred.loc[~df_pred.index.isin(nw_indices)].copy()

  return df_test, df_pred


if __name__ == "__main__":
  df_test = pd.DataFrame({'Image': list('abcd'), 'Id': list('abbz')}).set_index('Image')
  df_train = pd.DataFrame({'Image': list('efgh'), 'Id': list('cabb')}).set_index('Image')

  print(df_test.head())
  print(df_train.head())

  df_test = update_new_whales(df_train, df_test)

  assert (df_test.loc['d'] == 'new_whale').all()