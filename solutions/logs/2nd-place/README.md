#Experiments and training steps

This is the list of training steps and experiments done for analyzing the second place solution.

## Training step logs

### ResNet-101

Training procedure logs for each type of training involving ResNet-101.

- [256x512 - pseudo labels](./resnet101.pseudo.256x512.log) - This was the first training performed. It target training using image size 256x512 and pseudo labeled data. For the complete log, including the model structure, see the [screen log](/screen-resnet101.pseudo.256x512.log).

- [256x512](./resnet101.256x512.log) - Training using the image size 256x512 without pseudo labels. It was used a batch size of 64.
- [512x512 - pseudo labels](./resnet101.pseudo.512x512.log) - Model using image size 512x512 with pseudo labels. Batch size was set to 16, since a single GPU was used.
- [512x512](./resnet101.512x512.log) - Model using image size 512x512 without pseudo labels. Batches sized 16, and a single GPU was used.

### SE-ResNet-101

- [256x512](./seresnet101.256x512.log) - Model trained using images with 256x512 size without pseudo labels. For this training, a batch size of 64 was used, since all GPUs were available for usage.
- [256x512 - pseudo labels](./seresnet101.pseudo.256x512.log) - Model trained as the same item but with pseudo labels.

## Experiments

