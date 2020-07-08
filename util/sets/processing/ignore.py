from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd

class IgnoreProcessing():
  def __init__(self, files=[]):
    frames = []

    for file in files:
      if file is None:
        continue
      
      frames.append(pd.read_csv(file))

    if len(frames) > 0:
      self.filter_df = pd.concat(frames).set_index('Image')
    else:
      self.filter_df = None

  def apply(self, df):
    if self.filter_df is not None:
      df = df.drop(self.filter_df.index, errors='ignore')

    return df

if __name__ == "__main__":
  images = list('abcd')
  remove = list('ad')

  df = pd.DataFrame({'Image': images, 'Id': list('wxyz')}).set_index('Image')

  ignore = IgnoreProcessing()

  ignore.filter_df = pd.DataFrame({'Image': remove}).set_index('Image')

  assert len(df) == 4

  df = ignore.apply(df)

  assert len(df) == 2
  assert all([x in df.index for x in images if x not in remove])
  assert all([x not in df.index for x in remove])
