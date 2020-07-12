# Submissions

This solution had a single submission, the [post-processed submission](./submission.processed.csv). This model consisted in the ensemble of the three configuration files in the [configuration folder](../config). All of them used the DenseNet-121 as the backbone network, and had slightly changes on the learning rate schedule. Moreover, the 3rd configuration used a different set of labels for training, more specifically the [train.v2.csv set](../data/train.v2.csv).

## Result

| Leaderboard  | Score     |   
|--------------|-----------|
| Public       | 0.96984   |   
| Private      | 0.96889   |   

