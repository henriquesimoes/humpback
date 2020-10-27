# Dataset correction

This folder contains both the data curation files (intermediate files used by us) and the dataset splits used in our
experiments.

## Data curation

As part of our examinination on the dataset, we selected from the [Kaggle forum][1] issues found by competitors regarding labels.
The main issues were duplicate classes and mislabeled examples (either as a different identifiable class or as the _new whale_
class). Our inspection results are available on the [filter directory](./filter), which has the following files:

- [create_dirs.sh](./filter/create_dirs.sh) - This bash script was used to create the environment used to inspect the
dataset. It places all examples separated by classes, merging potential duplicate classes into the same directory. The
script has an option that includes the original class in the file name to ease checking whether images are really from
different classes or not. It uses [create_dirs_by_id.py](./filter/create_dirs_by_id.py), which does the real job.
- [duplicate_imgs.csv](./filter/duplicate_imgs.csv) - This file cointains a list of pairs of images that are duplicated,
i.e. the same photograph in two different files. The CSV columns indicate which image we have chosen to keep and which
we have removed from our corrected dataset.
- [hard.csv](./filter/hard.csv) - This file lists all image files we found where a _difficulty_ factor existed.
These factors include:
    - Occlusion (submerged or water aspersion);
    - Poor photograph angle;
    - Poor image resolution (_e.g._ blur, photographed from far way);
- [mislabeled.csv](./filter/mislabeled.csv) - Mislabeled examples found and their corresponding correct class. In some
cases, we found just one example which did not belong to the assigned class. In such situations, we listed the image
correct label as `new_id`. In our corrected dataset, this label turned into `new_whale`. For more information about the
dataset creation process, check the section [Splits](#splits).
- [new_groups.csv](./filter/new_groups.csv) - This file contains a list of _new whale_ examples that are actually the same
whale. We did not make use of this list, though. We decided to keep them all as _new whales_.
- [not_new.csv](./filter/not_new.csv) - Potentially mislabeled _new whales_ and our conclusions about them.
- [not_valid.csv](./filter/not_valid.csv) - Examples we considered not appropriate to include in the corrected dataset.
The most frequent factor was multiple flukes in the same image file (either from the same whale or from other whales).
- [texted.csv](./filter/texted.csv) - Image files that contain some type of textual information on them. The most
frequent situation is hand-written or typed information in a white box on the bottom of the image.
- [duplicates](./filter/duplicates) - Duplicate tuples found in the Kaggle forum (`raw`), and its compressed version,
which merges multiple (redundant) occurrences. 

## Splits

The dataset splits devoted 20% of the data for test and 80% for training. In our experiments, we
used two random samplings, which formed two tests. To generate these tests, we used the
[create_sets.sh](./create_sets.sh) script, which uses the [data curation files](#data-curation).
As can be seen, we allowed the [hard set](./sets/hard.csv) include the texted images. In addition, we removed the invalid
and duplicate images from the corrected set.

The resulting test and train CSV files are available in the `sets` folder, along with a
[stats file](./sets/tests.stats.log). The updated class list is available in the [classes.csv](./sets/classes.csv) file
to facilitate the evaluation and configuration of the trained models.

[1]: https://www.kaggle.com/c/humpback-whale-identification/discussion
