# Training logs

These training logs refer to the test #2 dataset. For this reason, the seventh split has been used. A single complete training was done, which had the following training steps:

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
    - From checkpoint 55800
        - Training MAP@5: 0.9988
        - Validation MAP@5: 0.4657
    - [Log file](./train.1.1.log)
3. Fine-tuning training phase
    - Freezed
    - All classes
    - Learining rate lr = 3e-5
    - Batch size: 3
    - From checkpoint 106200
        - Validation MAP@5: 0.6167
    - [Log file](./train.1.1.1.log)
4. Result:
    - Checkpoint: 106600
        - Validation MAP@5: 0.6360
