# Input data

This file have been created to document the splits used in our experiments.

## Labels

Since our own train and test datasets have been built, the labels have changed slightly. Thus, we have updated it to be able to reevaluate the first solution. Now, the previous [labels](./label.csv) have been updated to [the new labels](./new_label.csv) on the [reader script](../dataSet/reader.py).

## Splits

In our tests, two different dataset configuration have been used. Thus, splits with respect to these tests had to be built. In order to use the 1st placed team code without many changes, two extra splits have been created using the [generate_valid.py](./generate_valid.py) code. We used approximately the same proportion of examples in the validation, which is around 2.925%. Therefore, we obtained two new splits:

- Split 6: Train and validation splits relative to the [test #1](../../../test/sets/test#1/train.csv) training dataset.
- Split 7: Train and validation splits relative to the [test #2](../../../test/sets/test#2/train.csv) training dataset.
