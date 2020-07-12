from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd

class DatasetBuilder():
  def __init__(self, df_standard, df_hard=None, test_percentage=0.2):
    self.df = df_standard
    self.df_hard = df_hard
    self.test_p = test_percentage

  def build(self):
    df_test = self.df.sample(frac=self.test_p)
    df_train = self.df[~self.df.index.isin(df_test.index)]

    return df_train, df_test

