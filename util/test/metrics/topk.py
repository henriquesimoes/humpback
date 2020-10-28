from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch


def precisionk(actual, predicted, topk=(1, 5)):
    """
    Computes the precision@k for the specified values of k.

    # Parameters

    actual : `Sequence[Sequence[int]]`, required
      Actual labels for a batch sized input.
    predicted : `Sequence[Sequence[int]]`, required
      Predicted labels for a batch sized input.
    topk : `Tuple`, optional (default = `(1,5)`)
      Values of k to be computed.

    # Returns

    accuracy : `Sequence[float]`
      Accuracy result for given value of k in the given order.
    """
    actual = torch.LongTensor(actual)
    pred = torch.LongTensor(predicted)

    batch_size = pred.size(0)

    assert batch_size == actual.size(0)

    pred = pred.t()
    correct = pred.eq(actual.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].any(dim=0).view(-1).float().sum()
        res.append((correct_k * 1.0 / batch_size).item())

    return res
