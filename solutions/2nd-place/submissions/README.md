# Submissions

## Ensemble submission

This [classification](./2nd_ensemble.csv) was generated using Shen's specifications. This means the following trained models took part of the ensemble with their corresponding weights.

| Model          |         Image size      |     Pseudo labels      |          Weight          |
|----------------|-------------------------|------------------------|--------------------------|
| ResNet101      | 256x512<br><br>512x512  | YES<br>NO<br>YES<br>NO |  2 <br> 1 <br> 2 <br> 1  |
| SE-ResNet101   | 256x512<br><br>512x512  | YES<br>NO<br>YES<br>NO |  2 <br> 1 <br> 2 <br> 1  |
| SE-ResNeXt101  | 256x512<br>512x512      |        NO<br>YES       |         1 <br> 2         |

### Result

| Leaderboard     |     Score    |
|-----------------|--------------|
| Public          |   0.97150    |
| Private         |   0.96910    |
