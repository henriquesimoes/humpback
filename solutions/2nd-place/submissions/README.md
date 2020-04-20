# Submissions

## Ensemble submission

This [classification](./2nd_ensemble.csv) was generated using Shen's specifications. This means the following trained models took part of the ensemble with their corresponding weights.

| Model          |   Image size   |    Pseudo labels |   Weight   |
|----------------|----------------|------------------|------------|
|                |                |       YES        |      2     |
|                |   256x512      |------------------|------------|
|                |                |       NO         |      1     |
|  ResNet101     |----------------|------------------|------------|
|                |                |       YES        |      2     |
|                |   512x512      |------------------|------------|
|                |                |       NO         |      1     |
|----------------|----------------|------------------|------------|
|                |                |       YES        |      2     |
|                |   256x512      |------------------|------------|
|                |                |       NO         |      1     |
|  SE-ResNet101  |----------------|------------------|------------|
|                |                |       YES        |      2     |
|                |   512x512      |------------------|------------|
|                |                |       NO         |      1     |
|----------------|----------------|------------------|------------|
|                |   256x512      |       NO         |      1     |
| SE-ResNeXt101  |----------------|------------------|------------|
|                |   512x512      |       YES        |      2     |
|----------------|----------------|------------------|------------|

