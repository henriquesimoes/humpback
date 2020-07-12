# Submissions

## Individual models

Only one model has been submitted. This model might be considered the most complete and complex single model used by Shen.

### Result

| Model                                | Public leaderboard    | Private leaderboard   |
|--------------------------------------|-----------------------|-----------------------|
| SE-ResNeXt101<br>pseudo + 512x512    | 0.95647               | 0.95762               |

## Backbone network ensemble

Those submission were made to compare the different backbone networks used and the final ensemble.

### Result

| Model                    | Public leaderboard    | Private leaderboard   |
|--------------------------|-----------------------|-----------------------|
| ResNet101 ensemble       | 0.96825               | 0.96774               |
| SE-ResNet101 ensemble    | 0.96673               | 0.96640               | 
| ResNet101 ensemble       | 0.96754               | 0.96532               | 
 
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
