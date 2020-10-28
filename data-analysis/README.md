# Data Analysis

This folder contains processed information about some aspects of the dataset. We used to it to better understand the data,
including:
- [how the examples are distributed over the classes][1];
- [what is the image coloring distribution][2] (gray-scale or colored);
- [what is the range of image sizes in the testing and training sets][3];

The scripts used to generate these files can be found [here](../util/data-analysis). We also investigated [how
much contrast there existed in the examples][4]. The result was a script that directly generates histogram
charts.

[1]: ./classes.csv
[2]: ./color.csv
[3]: ./image-sizes
[4]: ../util/data-analysis/plot-images-constrast.py
