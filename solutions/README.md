# Solutions

In this folder we have the solutions' source codes cloned from their original
repositories. Check out the corresponding `README.md` files to find the
repository link or read the sections below.

Due to our dataset correction procedure (see [test sets description](../test/README.md)), some changes were
made in the solution branches. Thus, we will
describe here how to run the adapted solutions using [Docker][docker]. In our
experiments, we used the [`ufoym/deepo:all-py36-cu101`][deepo] Docker image, as it
is already configured with commonly used Deep Learning packages, and knows how to use
NVIDIA GPUs.

Note that all solution scripts are configured to always use GPUs.
Therefore, you will not be able to run the code without them.

## Creating test sets

First of all, we might want to create new data splits for training and testing
the solutions. Thus far, we have created only two such split sets ([`test#1` and
`test#2`](../test/sets/)).

To create test sets we will need the labels from the
competition, which are not in this repository. In the sequel, we will show how to
download the necessary data and how to create splits.

### Downloading the data

Since this dataset is part of a  Kaggle competition, you will need
to have an account with Kaggle to be able to read (and accept) the data usage terms before
downloading the data. Updated instructions to download the
data can be found in the 'Data' tab of [this competition's page][competition] . 
In our installation, we have already downloaded these data at:

```txt
/data/$USER1/hwic/competition-data/
```

where `USER1` is the first user in our group who dealt with the data.
You may copy them to your homedir.  Create a new directory somewhere
in your homedir and copy the image files and labels there:

```bash
cp -r /data/$USER1/hwic/competition-data/train $HUMP/data/
cp /data/$USER1/hwic/competition-data/train.csv $HUMP/data/
```

whwre `HUMP` is the directory you just created.
The `.gitignore` file is set to ignore them, in
order to avoid potential issues when switching branches.

From now on, we will assume the files are placed as described here.

### Creating splits

A Python script is available in the
[`util/sets`](../util/sets) folder for split creation. It accepts
several parameters related to our data curation process, including which
classes are duplicated, which images are wrongly classified as `new_whale` and
so on (click [here](../test/README.md) for a complete list).

Before executing the command, we need to make sure all Python package
dependencies are satisfied. For this, we recommend using [a virtual
environment][venv], since it avoids messing up other configurations in
your development environment.  After configuring our virtual env, run

```bash
  pip3 install -r util/sets/requirements.txt
```

Now, to create the testing sets as we have done for the first two tests, you can
use the following command:

```bash
cd test
dest=<dest>
mkdir $dest
python3 ../util/sets/create_sets.py \
  --labels ../data/train.csv \
  --remove filter/not_valid.csv \
  --hard filter/hard.csv,filter/texted.csv \
  --duplicate-images filter/duplicate_imgs.csv \
  --duplicate-classes filter/duplicates/duplicates.csv \
  --not-new filter/not_new.csv \
  --mislabeled filter/mislabeled.csv \
  --test_percentage=0.2 \
  --tests=<n> \
  --output=$dest \
  > $dest/tests.stats.log
```

replacing `<n>` by the number of tests you want to create and
`<dest>` by the destination folder (use something different from `sets` if you do
not want to overwrite the current sets in the repository). The above command
redirects the output to the `tests.stats.log` file inside the `<dest>` folder,
storing information about each test. Note that these commands are similar
to the ones available in [`create_sets.sh`](../test/create_sets.sh).

## 2nd solution

This solution was cloned from [this repository][2nd-repo]. The first step to execute
the 2nd placed solution is to go to its corresponding branch, _i.e._
`2nd-solution`. There, we can find the adapted code for running the solution
with [our generated test sets](#creating-test-sets).

### Creating validation sets

Following common practice, this solution uses a small part of the training set for
validation. The information of which examples will be used for training and
which will go for validation was included in text files by the author,
considering the competition dataset. Therefore, they are invalid for our
experiments. We adapted the scripts to assume that there are files describing
the training and validation sets with the following name format
inside the `image_list` folder:

```txt
test{n}.{valid|train}.txt
```

where `{n}` is the test number (so far, 1 and 2 exist) and `{valid|train}` is
either `valid` for validation set or `train` for training set. These files can
be generated for new test sets using the `create_validation.py` script inside
the `image_list` folder. For test #3, for instance, you can run

```bash
cd solutions/2nd-place/image_list
python3 create_validation.py \
    --train ../../../test/sets/test\#3/train.csv \
    --test_number 3
```

By default, it will use the same percentage split as the author of the solution.

### Creating the container

Instead of having a Docker image for each solution, we will follow a different
approach here. First, we will create a container based on the `deepo` image with
volumes and then execute the solution inside it. To do this, we will use the
detach flag (`-d`) from `docker run`, which allows the container to run
independently from the current bash process, and, as we launch it, we will
already get into it using the interactive flags (`-it`).

Since these solutions use a significant among of memory, we will have to extend
the amount of shared memory for the container. To do so, we can use the
`--shm-size=<amount>` flag. It is enough to give 8GB.

As stated before, we will need GPUs to run the solutions. To allow the container
to access the hardware, we must specify both the runtime (`--runtime=nvidia`)
and which GPUs to let visible to the container (through the `--gpus` flag). If
we want to let all GPUs available, we can use the `--gpus all`. If only a single
GPU should be used, say the second one, we can pass `--gpus device=1` (note that
GPU numbers start at 0). For two GPUs, say 2nd and 3rd GPUs, a more cumbersome
value must be given: `--gpus device='"device=1,2"'`. Yes, there are two level of
quotes in there. For more information, check out the discussion in the [NVIDIA
Docker repository on that][nvidia-docker#1257].

As we will see later, there is no problem in always specifying the `--gpus all`
to the create the container, as the GPU visibility can still be configured for
processes using the `CUDA_VISIBLE_DEVICES` environment variable. It is indeed a
better option if you are using a shared machine to run the experiments, as the
available GPUs might change over time, and that would require recreating the
container every time that happens.

Moreover, we will create [Docker volumes][docker-volumes] to map some
directories inside the container to the machine filesystem. This is interesting
to avoid copying too much data (~25K images) inside the container. We will do
the same for the source code and checkpoints that will be create when training.
Since the source code is mapped, you **should not** switch branches when the
code is in fact running.

Putting those altogether and assuming you execute the command at the repository
root, the resulting command looks like this

```bash
docker run -d -it \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_2nd \
   -v $(pwd)/data:/dataset \
   -v $CHECKPOINT_PATH/2nd-place/models:/solutions/2nd-place/models \
   -v $(pwd)/solutions/2nd-place:/solutions/2nd-place \
   ufoym/deepo:all-py36-cu101
```

where `$CHECKPOINT_PATH` is an environment variable specifying the path in the
host filesystem to store the checkpoints. For doing so, you can use:

```bash
export CHECKPOINT_PATH=/path/to/disk/folder
```

As checkpoints might be rather large (~7GB for experiment), a large storage disk
device should be used. All path specified inside the container (after the colon
`:` in the volume `-v` flags) should be kept as they are, since the source code
is configured to look after them when executing.

Note that we have given the `humpback_2nd` name for the container. It could be
any name, but we will assume that is its name from now on.

After executing that command, we will get a `bash` prompt which is at the root
directory of the container. There must be `solutions/2nd-place` and `/dataset`
folders in there, which are mapped to the machine, as we have seen. Make sure
the files are as expected. Since we used the detach option, you can get back to
the host machine any time by issuing either the `exit` command in the shell
terminal or typing `<ctrl> + <d>`. To get back inside a running container, we
can use the following command:

```bash
  docker exec -it humpback_2nd bash
```

When we run a longstanding command, such as when training the model, we would
not be able to get outside the container. However, this is impractical. Thus,
for such situations, we will use a handy Unix program called `screen`. It is not
available by default in `deepo`. Thus, we must install it with

```bash
  sudo apt install screen
```

Basically, this utility allows us to emulate a terminal. This makes possible to
detach from bash and exit the container whenever we want without killing the
process running in `screen`. We will show some steps on how to use it in later
sections. For a detailed explanation on how it works, see its man page.

Note that these steps can be done once for a set of experiments. There is no
problem in keeping the container alive when no training or inference is running.
When that is the case, you can stop the container with

```bash
  docker stop humpback_2nd
```

to avoid unneeded resource consumption. It will stop the container, but all data
inside it (whether it is mapped or not) will still exist. For removing the
container for good, you may use

```bash
  docker rm humpback_2nd
```

Note this will not delete the data from the mapped directories, just as indented.
However, it does remove all data strictly inside the container.

Now, we are ready to see both how to execute the training and inference
procedures.

### Training

Here we will describe how to run the training procedure for a given test set.
First, let us see how to set up the data, and then how to run the code.

#### Configuring the data

For running the training procedure, we will start with configuring the data to
be used. An important aspect to note here is that the solution code assumes
there are two directories in the container with the data in them:

- `/dataset/train`: data for training;
- `/dataset/test`: data for testing (not seen when training);

Note though that those should not be the original Kaggle datasets. That is
because part of the training data will now be used for testing the solutions.
Thus, the `test` folder should contain (or map somewhere that contains) the
images of the testing split.

As we have seen, 2nd solution uses files to list which files should be used for
training and which for validation. This means that it will only load the images
described in there. This allows us to let the `train` folder just as it comes
from Kaggle.

Something quite different happens for testing data. Here we will need to create
a `test` folder that contains the images we are willing to inference. Suppose we
are interested in training test number 1. Thus, we need to place all images
listed in `test/sets/test#1/test.csv` into the `test` folder. Instead of
literally copying the files, we can use symbolic links, saving disk storage. To
do so, you can use

```bash
  cd baleias/humpback/data
  mkdir -p test
  cat ../test/sets/test\#1/test.csv | grep -v "Image" | cut -d',' -f1 | xargs -i ln -s ../train/{} test/{}
```

This command takes each line in `test.csv` and runs `ln -s` to link
`test/<image>` to `train/<image>`. See `xargs` man page for more details on how
to use it.  Before that, we remove the header with `grep` and remove the class with `cut`.

If we wish to run the inference for the hard set instead, all we need to do is
change the origin file to `../test/sets/hard.csv`. Make sure you have `test`
directory empty before running the symbolic linkage, as all files from the
folder will be part of the inference process in this solution. You can delete
all previous symbolic links with `rm -r test`. That does not affect the files
they are referring to.

Recall that the `/dataset` folder inside the container is a volume that is
mapped to the repository `data` folder. We could also do that inside the
container. That is a matter of choice. Just bear in mind that all created files
will belong to the root user this way, since Docker runs in privileged mode.

#### Running

Now, we are ready to execute the training. Recall that, to get back to the
container, you should use:

```bash
  docker exec -it humpback_2nd bash
```

Once back into it, we will navigate to the source code. It is located at
`/solutions/2nd-place`. Thus, we use

```bash
  cd /solutions/2nd-place
```

As we have said previously, we would like to get out of the container after
issuing the training command. Thus, know we are going to get inside a `screen`
section. Yes, here are getting are two levels always from the original process,
that is, we are inside a screen section, which in turn is inside a container!

To do so, we can simply issue

```bash
  screen
```

But, it turns out it might be interesting to know what has happened when we were
out. (Screen does not have a friendly way of scrolling backward in the output,
as far as the authors know.) To do so, we will also specify a flag to log
everything in a log file, leading us to the following command

```bash
  screen -L -Logfile screen.log
```

Flag `-L` says to start logging right away, and `-Logfile` specifies which file
should be used (it does not need exist). This will therefore create `screen.log`
file in `solutions/2nd-place`, which is actually mapped to the host namesake
folder.

Now, we will launch `main.py` with `--mode train` option. But, we should also
specify other options as well, including model, image size, batch size and test
index (which is actually named `fold_index`). The command should look like this

```bash
CUDA_VISIBLE_DEVICES=0,1,2 python main.py \
  --mode=train \
  --model=resnet101 \
  --image_h=256 --image_w=512 \
  --fold_index=1 \
  --batch_size=64
```

An important note here is that we are specifying for the running process that it
will be able to access GPUs 0, 1, and 2. These GPU numbers may be different from
the host machine if you have used `--gpus` different from `all` previously. If
you did use `--gpus all`, they are the same. Here is when you check out which
GPUs should really be used, that is, which have enough free memory to run the
training procedure, and adapt the batch size accordingly. When running in a GPU
with about 10GB of free memory, a batch size 32 works fine.

It turns out some of the options we specified previously are already configured
by default. Thus, we may simplify the command to

```bash
CUDA_VISIBLE_DEVICES=0 python main.py \
  --mode=train \
  --fold_index=1 \
  --batch_size=32
```

if we are willing to run in the first GPU and in test split number one
(`fold_index=1`). You should set them to a different values if other
configuration is needed.

If all configuration went just fine, this command should print out information
about the network, and then continuously printing some statistics about the
training steps. When that happens, we can detach by typing `<ctrl> + <a>`
followed by `<d>`. And then securely `exit` the container.

During the training procedure, the code will save model checkpoints in the
`resnet101_test0_256_512` folder inside `solutions/2nd-place/models`, which we
mapped to `$CHECKPOINT_PATH`. The name automatically changes as test index
changes. Moreover, it will create a statistics file named `log.train.txt` inside
the same folder. That file is important for us to draw loss and score curves.
Thus, it should be kept.

This step will take about a day to complete using an Intel Xeon Silver 4110 Octa
Core 2.10GHz processor and a single NVIDIA GeForce RTX 2080 Ti GPU.

### Inference

For inference, we are going to use one of the checkpoints saved during the
training procedure: the maximum validation one. It is automatically saved during
training, and is named `max_valid_model.pth`. Therefore, we will specify this
name for the `--pretrained_model` argument when running inference. This
essentially what changes from the command we have seen for triggering the
training procedure. Of course, we will also change `--mode` to `test`. Thus, the
command will look like this

```bash
CUDA_VISIBLE_DEVICES=0 python main.py \
  --mode=test \
  --fold_index=1 \
  --batch_size=32 \
  --pretrained_model=max_valid_model.pth
```

As we have done when training, we should issue this command inside the
container. Check out the [running section](#running) on how to do it. (Since
this step is far quicker than training, using `screen` is not actually needed
here.)

This solution uses Test-Time Augmentation (TTA) for dealing with flipped images
during test time. Therefore, two sets of inferred labels are produced and stored
in the `2TTA` folder inside the model checkpoint directory. To assemble these
results, `ensemble.py` script must be executed, generating the final
classification. To use it, you should run

```bash
  python3 ensemble.py --name resnet101
```

It will use by default `--checkpoint=max_valid_model` and `--threshold=0.185`
(this threshold value is used to decide what to consider a `new_whale`). Note
this command is different from the one written by the solution author, in which
an ensemble of several models (with different architectures) would be created.

A final CSV file will be generated, named `result.csv`. This is what we will
[later](#assessing-results) use to assess how the network has performed.

## 3rd solution

This solution was cloned from [this repository][3rd-repo]. Again, you should
move to its corresponding branch, _i.e._ `3rd-solution` before continuing the
following steps.

### Setting up the labels

This solution used CSV files to specify which labels to use for training. Thus,
we place the corresponding file in the `data` folder with a name which will
actually specify in a configuration file. We have followed the pattern
`test<n>.{train,sample}.csv` for conventional test sets, and `hard.sample.csv`
for the hard training set. Training file is pretty much the one we have
[generated before](#creating-splits). Just copying it must do. Test image
listing (`sample`) file should be like `sample_submission.csv` from Kaggle. But
the solution code do not actually care about the content in `Id` column. So we
can change it to something shorter than 5 classes. For instance, we can generate
such file the following way.

```bash
  dest_file=solutions/3rd-place/data/test3.sample.csv
  echo "Image,Id" > $dest_file
  cat test/sets/test\#3/test.csv | \
    grep -v Image | \
    cut -d, -f 1 | \
    xargs -i echo {},ids >> $dest_file
```

This first adds the `Image,Id` header to the file. Then, it gets each line from
`test.csv` that does not contain the `Image` keyword (all but the header), cut
it by the comma, takes the image name field (`-f 1`) and appends it (`>>`)
followed by `,ids` to the destination file. We could simply copy the `test.csv`
file as `test3.sample.csv` file. But we then would need to be more careful about
data leakage. It turns out to be better to replace the labels to `ids`.

As we have said before, these files we have created could have any naming. This
is because we need to configure a YAML file with the parameters of the model. In
this file, we will also specify both training and testing label files. For each
different experiment, a configuration file should exist in `configs/`. In fact,
the ones we have used are therein. To reproduce what we have done, copy one of
them (_e.g._ `cp test1.yml test3.yml`) and update its first lines to match the
label files. For example, it should look like this for our example for test #3.

```yml
data:
  name: 'IdentificationDataset'
  dir: 'data'
  params:
    train_csv: 'test3.train.csv'
    sample_csv: 'test3.sample.csv'

# and the file goes on unchanged from here...
```

We will update other option in this file in the next section. But this is all we
have to do to configure the labels.

Finally, to let the images listed in `test3.sample.csv` available during the
inference process, we would need to place them in `data/test`. It turns out that
the code will only load the images listed in the file. Thus, all we actually
need to do is to symbolically link the `train` folder itself to `test`, such as
in

```bash
  ln -s data/train data/test
```

Note this configuration conflicts with the one presented for the second
solution. Thus, double check everything before continuing.

### Training steps

During training, information about checkpoints and statistics are created. These
are placed in a directory specified in the config file as well. Thus, we will
need to update its contents (from the previous section). Look for a `train:`
property in the file, and update it accordingly. For instance, for our test #3
example it could look like this

```yml
# ... other properties appear up here

train:
  dir: './train_logs/test3'
  batch_size: 32
  log_step: 200
  save_checkpoint_epoch: 2
  num_epochs: 300

# and it continues below...
```

Note here we already specifying the batch size to be used, as well as the number
of epochs. They should be kept this way for reproducing the pipeline we have
followed. This batch size should be fine to run in single GPU with about 10GB of
free memory.

#### Building the container

Here we take very close approach to [the one explained for the second
solution](#creating-the-container).

Since the path we specify in `train.dir` is used to store checkpoint files, it
is interesting to have it mapped to a folder in a large storage disk. We will
again assume the `$CHECKPOINT_PATH` environment variable points to an
appropriate path in such disk.

In addition, we will map the `data` directory a bit differently. This time, we
will make it be inside the solution folder, since the YAML file specifies a
relative path.

The resulting command is

```bash
docker run -d -it \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_3rd \
   -v $(pwd)/solutions/3rd-place:/solutions/3rd-place \
   -v $CHECKPOINT_PATH/3rd-place/train_logs:/solutions/3rd-place/train_logs \
   -v $(pwd)/data:/solutions/3rd-place/data \
   ufoym/deepo:all-py36-cu101
```

This step need to be done just once (as long as the container still exists).

#### Start training procedure

As we have done before, we will need once again to use `screen` to run the
training procedure. So launch it inside the container and change to directory
`solutions/3rd-place`. After that, we can start training by simply issuing

```bash
  export CUDA_VISIBLE_DEVICES=0
  python3 train.py --config=configs/test3.yml
```

to start training with the configuration specified by `test3.yml`. This might
take around 4 days using a single GPU (10GB free memory).

After this process, several checkpoints are created. For the next steps, we are
going to assume `$CUDA_VISIBLE_DEVICES` is set accordingly. We still need a few
steps before generating the classification.

#### Stochastic Weight Averaging

This solution uses the strategy proposed by [Izmailov and colleagues
(2018)][swa-paper], which basically consists in averaging the network (internal)
weights of epochs close to the convergence point. Thus, we will use `swa.py`
script to perform this averaging in the parameters saved in disk during the
training procedure.

To do so, we can simply use

```bash
  python3 swa.py --config=configs/test3.yml
```

#### Computing similarities

Now that the averaged model is available, we can compute the similarities among
training and test images. For doing so, we will need to execute the following
script:

```bash
  mkdir -p similarities
  python inference_similarity.py \
    --config=configs/test3.yml \
    --tta_landmark=0 \
    --checkpoint_name=swa.pth \
    --output_path=similarities/test3.csv
```

Note we are setting it not to perform test-time augmentation for the different
landmarks the author has created, and thus simplifying the inference process.

#### Generating predictions

Finally, to generate the classification, all we need to do is select the most
similar whale classes based on the precomputed similarities. To do so, we will
now use the following command:

```bash
  python3 make_submission.py \
    --threshold=0.385 \
    --input_path=similarities/test3.csv \
    --sample_path=data/test3.sample.csv  \
    --output_path=results/test3.csv
```

Threshold value have been defined by the solution author and thus should be
kept. It basically decides which similarity score is low enough to classify a
whale as new. As the other solutions, this generates a CSV file containing the
predictions, which is `test3.csv` in this case.

## Assessing the results

After solution CSV prediction files had been generated, the authors would submit
them to Kaggle to check against the ground truth labels for testing set and
compute the Mean Average Precision at 5 (MAP@5). As we cannot specify which set
of images and labels Kaggle should use, we have implemented the metrics in our
own for evaluating the classification. The implementation is available at
[util/test](../util/test).

To use this utility, we should give it at least four arguments:

- `--test`: path to test CSV file from the corresponding experiment (generated
  in [splits](#creating-splits)). It may be the `hard.csv` file as well;
- `--train`: path to `train.csv` file from the corresponding experiment;
- `--prediction`: path to file that generated by the solution to be evaluated;
- `--classes`: path to `classes.csv` (also generated by the split script);

This will produce a report file, containing the results for each some metrics
implemented by us, including MAP@5. Since we intend to keep this file as a
report from the solution, there are a few arguments to describe the experiment
that was performed. They are

- `--name`: Dataset name, for instance, `Test #3`;
- `--solution`: Solution name that produced the prediction, _e.g._ `2nd
  solution`;
- `--description`: Brief description of the model, _e.g._ `ResNet-101 (512x256)
  trained 100 epochs`

We may also specify where to output with the `--report-output` argument. Thus, a
usual usage of the script would be something like:

```bash
  python3 util/test/test.py \
    --name "Test #3" \
    --solution "2nd solution" \
    --description "ResNet-101 (512x256) trained 100 epochs" \
    --classes test/sets/classes.csv \
    --test test/sets/test\#3/test.csv \
    --train test/sets/test\#3/train.csv \
    --prediction solutions/2nd-solution/results/test3.csv \
    --report-output solutions/2nd-solution/results/test3.md
```

Note that here we are assuming the prediction CSV file to be inside `results`
folder of the corresponding solution. This is how we have done for the
experiments run so far. Moreover, we specified a Markdown extension for the
output file, as reports follow its specification (and are nicely rendered in
GitHub).

[2nd-repo]: https://github.com/SeuTao/Kaggle_Whale2019_2nd_palce_solution
[3rd-repo]: https://github.com/pudae/kaggle-humpback

[competition]: https://www.kaggle.com/c/humpback-whale-identification

[venv]: https://docs.python.org/3/library/venv.html
[docker]: https://www.docker.com
[docker-volumes]: https://docs.docker.com/storage/volumes/

[swa-paper]: https://arxiv.org/abs/1803.05407
[deepo]: http://ufoym.com/deepo/
[nvidia-docker#1257]: https://github.com/NVIDIA/nvidia-docker/issues/1257
