# Training on test#2 dataset

Training attempt using the following configurations:

- Dataset: test #2 (fold index = 2)
- Backbone network: ResNet-101
- Image size: 256x512
- Batch size: 32
- Epochs: 100

Maximum validation reached on the:

- iteration: 73799;
- epoch: 50;
- time: 15h50;

having the following scores:

- Top@1: 87.169
- Top@5: 88.624
- MAP@5: 0.878747795414462

Training logs are available on the [log file](./train.log).
