from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd

class LabelProcessing():
  def __init__(self, mislabeled=None, not_new=None):
    self.df_mislabeled = pd.read_csv(mislabeled).set_index('Image') \
      if mislabeled is not None else None
    self.df_not_new = pd.read_csv(mislabeled).set_index('Image') \
      if mislabeled is not None else None
    
  def apply(self, df):
    if self.df_mislabeled is not None:
      df = self._fix_mislabeled(df)
    if self.df_not_new is not None:
      df = self._fix_not_new(df)
    return df
  
  def _fix_mislabeled(self, df):
    replace = self.df_mislabeled[self.df_mislabeled['Correct'] != 'new_id']
    generate = self.df_mislabeled[self.df_mislabeled['Correct'] == 'new_id']
    
    indexes = replace.index.intersection(df.index)
    df.loc[indexes, 'Id'] = replace.loc[indexes, 'Correct']

    # TODO: check whether new ids will be generated or the new_whale class will
    # be used instead

    indexes = generate.index.intersection(df.index)
    df.loc[indexes, 'Id'] = 'new_whale'

    return df

  def _fix_not_new(self, df):
    return df

def test_mislabeled():
  original = list('axy')

  df = pd.DataFrame({'Image': list('abcd'), 'Id': list('aaaa')}).set_index('Image')

  processing = LabelProcessing()

  mislabeled = {'Image': list('acd'), 'Correct': ['new_id'] + list('xy')}
  processing.df_mislabeled = pd.DataFrame(mislabeled).set_index('Image')

  assert len(df) == 4

  df = processing.apply(df)

  assert len(df) == 4

  for image, correct in zip(*mislabeled.values()):
    if correct is 'new_id':
      assert df.loc[image]['Id'] is 'new_whale'
      # assert df.loc[image]['Id'] != 'new_id'
      # assert df.loc[image]['Id'] not in original
    else:
      assert df.loc[image]['Id'] == correct

def test_not_new():
  pass

if __name__ == "__main__":
  test_mislabeled()
  test_not_new()
