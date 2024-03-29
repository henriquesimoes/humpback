# Log files for trainings and experiments

## Training steps

All the training log has been kept in this folder, even if they haven't been used in further training attempts.

### First step

The first training step consists in the training using only images of whales that had more than 10 examples in the training dataset, with the whole net unfrozen.

1. [train.1.log][1] - First training attempt using only the original dataset, with batch size 3;
2. [train.2.log][2] - Training attempt using the same configuration as the first one, except from the batch size which was set to 5;
3. [train.3.log][3] - Training that expected to use the playground images to be trained. However, by now, we've noticed it actually didn't use the playground examples at all, once the configured fold was the 1st one;
4. [train.4.log][7] - Training using playground images by using the second fold;

### Second step

In this step, the minimum number of examples per class used was set to zero, with the whole net freezed but the last layers.

1. [train.2.1.log][4] - Second training step using the best checkpoint (#22600) from 2nd attempt in the first step;
2. [train.2.2.log][5] - Training using the same checkpoint as the previous one but using the playground data;
3. [train.4.3.log][8] - Training using the checkpoint #11000 (0.980) from the fourth attempt on 1st step, also using the second fold;
4. [train.4.4.log][9] - Training using checkpoint #26000 (0.992) from 4th attempt on 1st step, using the playground data (2nd fold);

### Third step

1. [train.2.1.1.log][6] - First training on 3rd step, using the best checkpoint (#66600) of the second step (2.1);
2. [train.4.4.2.log][10] - Last training step using the training tree branch 4.4 (checkpoint #70000 - 0.8130).

## Experiments

### Usage of playground images

We suspected after analyzing the folds (from 5-fold validation) files that the playground images weren't being used at all during the trainings we were doing. So, to validate this hypotesis, we changed the fold used by the algorithm to the 2nd fold, which included playground images in the labeling. Once the images were not included in the training images folder, the expected result would be the code being broken. The result was as expected, as the [experiment-2nd-fold.log][20] shows.

This way, we're now sure that the first fold didn't use any playground images, since otherwise it would have broken as well, but this wasn't what happened.

[1]: ./train.1.log
[2]: ./train.2.log
[3]: ./train.3.log
[4]: ./train.2.1.log
[5]: ./train.2.2.log
[6]: ./train.2.1.1.log
[7]: ./train.4.log
[8]: ./train.4.3.log
[9]: ./train.4.4.log
[10]: ./train.4.4.2.log

[20]: ./experiment-2nd-fold.log
