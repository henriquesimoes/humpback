# Submissions description

## 1st submission

Training steps:

- 1st step:
    - Fold index: 1
    - Freezing: False
    - Minimum number of class: 10
    - Learning rate: 3e-4
    - Batch size: 5
    - Reached MAP@5 training: 0.995
- 2nd step:
    - Fold index: 1
    - Freezing: True
    - Minimum number of class: 0
    - Learning rate: 3e-4
    - Batch size: 5
    - Checkpoint: 22600 of 2nd first step attempt
    - Reached MAP@5 validation: 0.8323
- 3rd step:
    - Fold index: 1
    - Freezing: True
    - Minimum number of class: 0
    - Learning rate: 3e-5
    - Batch size: 5
    - Checkpoint: 66600 of 1st second step attempt
    - Reached MAP@5 validation: 0.8620

Kaggle score:
    - Public leaderboard: 0.82299
    - Private leaderboard: 0.85070

## Second submission

The idea was try to train using the playground data in order to achieve a better generalization.

Training steps:

- 1st step:
    - Fold index: 2
    - Freezing: False
    - Minimum number of class: 10
    - Learning rate: 3e-4
    - Batch size: 5
    - Reached MAP@5 training: 0.992
- 2nd step:
    - Fold index: 2
    - Freezing: True
    - Minimum number of class: 0
    - Learning rate: 3e-4
    - Batch size: 5
    - Checkpoint: 26000 of 2nd first step attempt
    - Reached MAP@5 validation: 0.8130
- 3rd step:
    - Fold index: 2
    - Freezing: True
    - Minimum number of class: 0
    - Learning rate: 3e-5
    - Batch size: 5
    - Checkpoint: 70000 of 1st second step attempt
    - Reached MAP@5 validation: 0.8724

Kaggle score:
    - Public leaderboard: 0.84870
    - Private leaderboard: 0.86513
