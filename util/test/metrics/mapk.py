from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

def apk(actual, predicted, k=10):
  '''
  Computes the Average Precision at k (AP@k).

  # Parameters

  actual : `Sequence[int]`, required
    Actual labels for a single input.
  predicted : `Sequence[int]`, required
    Predicted labels a single input.
  k : `int`, optional (default = `10`)
    Value of k to be computed.

  # Returns

  avg_precision : `float`

  # Source
  
  https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/average_precision.py
  '''
  if len(predicted)>k:
    predicted = predicted[:k]

  score = 0.0
  num_hits = 0.0

  for i,p in enumerate(predicted):
    if p in actual and p not in predicted[:i]:
      num_hits += 1.0
      score += num_hits / (i + 1.0)


  return score / min(len(actual), k)

def mapk(actual, predicted, k=5):
  '''
  Computes the Mean Average Precision at k (MAP@k).

  # Parameters

  actual : `Sequence[Sequence[int]]`, required
    Actual labels for a batch sized input.
  predicted : `Sequence[Sequence[int]]`, required
    Predicted labels a batch sized input.
  k : `int`, optional (default = `5`)
    Value of k to be computed.

  # Returns

  map@k : `float`

  # Source
  
  https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/average_precision.py
  '''
  return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])

if __name__ == "__main__":
  actual = np.zeros((5,1), dtype=np.int32)
  pred = np.arange(10).reshape(5,-1)

  pred[:,1] = 0

  print([apk(a,p,k=2) for a,p in zip(actual, pred)])
  print(mapk(actual, pred, k=2))
