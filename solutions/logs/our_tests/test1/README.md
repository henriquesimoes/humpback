# Training logs

These training logs refer to the test #1 dataset. For this reason, the sixth split has been used. Two attempts have been done, but the second one did not have its final phase done, since the first attempt had a better result on the second step.

## First attempt

This attempt led to the final trained model, and consisted of the following steps:

1. Start up training phase, which had these settings:
    - Not freezed
    - Limited with classes with more than 10 examples
    - Learining rate lr = 3e-4
    - Batch size: 2
    - [Log file](./train.1.log)
2. Frozen training phase.
    - Freezed
    - All classes
    - Learining rate: 3e-4
    - Batch size: 3
    - From checkpoint 22200
        - Training MAP@5: 0.9912
        - Validation MAP@5: 0.4668
    - [Log file](./train.1.2.log)
3. Fine-tuning training phase
    - Freezed
    - All classes
    - Learining rate lr = 3e-5
    - Batch size: 3
    - From checkpoint 56600
        - Validation MAP@5: 0.5954
    - [Log file](./train.1.2.1.log)
4. Result:
    - Checkpoint: 57200
        - Validation MAP@5: 0.6338

## Second attempt

This attempt did not lead to a final trained model, but consisted of the following steps:

1. Start up training phase, which had these settings:
    - Not freezed
    - Limited with classes with more than 10 examples
    - Learining rate lr = 3e-4
    - Batch size: 2
    - [Log file](./train.2.log)
2. Frozen training phase.
    - Freezed
    - All classes
    - Learining rate: 3e-4
    - Batch size: 3
    - From checkpoint 46200
        - Training MAP@5: 0.9975
        - Validation MAP@5: 0.4679
    - [Log file](./train.2.1.log)
3. Not done
4. Partial result:
    - Best checkpoint: 95800
        - Validation MAP@5: 0.5834

## Failed attempt

This attempt refers to the second training step, which used the checkpoint 18800 from the first step of the first attempt. The [log file](./train.1.1.log) shows that the training got stuck on a poor validation place. This was probably caused by a very antecipated network freezing, failing its capacity to extract meaningful features from the images.
