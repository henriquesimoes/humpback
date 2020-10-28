from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


class Converter:
    def __init__(self, classes):
        self.id2int = {}

        for i, id in enumerate(classes):
            self.id2int[id] = i

    def to_numpy(self, df_pred, df_test):
        df_test.rename(columns={'Id': 'Actual'}, inplace=True)
        df_pred.rename(columns={'Id': 'Predictions'}, inplace=True)

        df = df_test.join(df_pred)

        actual_list = []
        pred_list = []
        for img, row in df.iterrows():
            actual = row['Actual']
            ids = row['Predictions'].split()

            actual_list.append([self.id2int[actual]])
            pred_list.append([self.id2int[id] for id in ids])

        return np.array(pred_list, dtype=np.int32), np.array(actual_list, dtype=np.int32)
