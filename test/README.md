# Dataset correction

This folder contains both the data curation files (intermediate files used by us) and the dataset splits used in our
experiments.

## Data curation

For examining the dataset, we selected from the [Kaggle forum][1] issues found by competitors regarding labels.
The main issues were duplicate classes and mislabeled examples (either another identifiable class or _new whale_
class). Our inspection result is available on the [filter directory](./filter), which has the following files:

- [create_dirs.sh](./filter/create_dirs.sh) - This bash script was used to create the environment used to inspect the
dataset. It places all examples separated by classes, merging potential duplicate classes into the same directory. All
examples may include their original class in the file name to easily check whether they're really from different classes
or not. It uses [create_dirs_by_id.py](./filter/create_dirs_by_id.py), which does the real job.
- [duplicate_imgs.csv](./filter/duplicate_imgs.csv) - This file includes a list of pair of images that are duplicated,
i.e. the same photograph in two different files. The CSV columns indicates which image we have chosen to keep and which
we removed from our corrected dataset.
- [hard.csv](./filter/hard.csv) - This files lists all image files we found that that a _difficulty_ factor existed.
These factors include:
    - Occlusion (submerged or water aspersion);
    - Poor photograph angle;
    - Poor image resolution (_e.g._ blur, photographed far way);
- [mislabeled.csv](./filter/mislabeled.csv) - Mislabeled examples found and their corresponding correct class. In some
cases, we found only a example which did not belong to the assigned class. In such situation, we listed the image
correct as `new_id`. In our corrected dataset, this label turned into `new_whale`. To more information about the dataset
creation, check the section [Splits](#splits).
- [new_groups.csv](./filter/new_groups.csv) - It contains a relation of _new whale_ examples that are actually the same
whale. This relation was not used by us, though. We decided to keep them all as _new whales_.
- [not_new.csv](./filter/not_new.csv) - Candidate examples of not being _new whales_ and our conclusion.
- [not_valid.csv](./filter/not_valid.csv) - Examples we considered not appropriate to include in the corrected dataset.
The most frequent factor was multiple flukes in the same image file (either from the same whale or from another whales).
- [texted.csv](./filter/texted.csv) - Image files that contain some type of texted information on them. The most
frequent situation is hand-written or typed information in a white box on the bottom of the image.
- [duplicates](./filter/duplicates) - Duplicate tuples found in the Kaggle forum (`raw`), and its compressed version,
which merges multiple (redundant) occurrences. 

## Splits

The dataset splits were generated considering the 20% of the data for test and 80% for training. In our experiments, we
used two random samplings, which formed two tests. To generate these tests, we used the
[create_sets.sh](./create_sets.sh) script, which uses the [data curation files](#data-curation).
As can be seen, we let the [hard set](./sets/hard.csv) include the texted images. Besides that, we removed the invalid
and duplicate images from the corrected set.

The resulting test and train CSV files are available in the `sets` folder, along with a
[stats file](./sets/tests.stats.log). The updated class list is available in the [classes.csv](./sets/classes.csv) file
to handle the evaluation and configuration of the trained models more easily.

[1]: https://www.kaggle.com/c/humpback-whale-identification/discussion
