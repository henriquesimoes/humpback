#!/bin/bash

IMAGE=humpback3

echo 'Train, test, and map model'
if [ "$#" != "4" ]; then
    echo "Usage: $0 HUMP CHKPT FOLD DEV"
    exit -1
fi

HUMP=$1
CHECKPOINT_PATH=$2
FOLD=$3
DEV=$4

##################################
### Setting up the labels
cd $HUMP
dest_file=solutions/3rd-place/data/test$FOLD.sample.csv
echo "Image,Id" > $dest_file
cat test/new-sets/test\#$FOLD/test.csv | grep -v "Image" | cut -d',' -f1 | xargs -i echo {},ids >> $dest_file

##################################
### Configuration yml
sed "s/test1/test$FOLD/" < solutions/3rd-place/configs/template.yml > solutions/3rd-place/configs/test$FOLD.yml

##################################
### Symbolic links
ln -s train data/test
 
###########################################
### TRAIN
read -r -d '' TRAINCMD << EOM
CUDA_VISIBLE_DEVICES=0,1,2 python3 train.py \
   --config=configs/test$FOLD.yml
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_3rd \
   -v $CHECKPOINT_PATH/3rd-place/train_logs:/solutions/3rd-place/train_logs \
   -v $(pwd)/solutions/3rd-place:/solutions/3rd-place \
   -w /solutions/3rd-place \
   $IMAGE bash -c "$TRAINCMD > train$FOLD.out"

###########################################
### Stochastic Weight Averaging
read -r -d '' SWACMD << EOM
CUDA_VISIBLE_DEVICES=$DEV python3 swa.py \
  --config=configs/test$FOLD.yml
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_3rd \
   -v $(pwd)/data:/solutions/3rd-place/data \
   -v $CHECKPOINT_PATH/3rd-place/train_logs:/solutions/3rd-place/train_logs \
   -v $(pwd)/solutions/3rd-place:/solutions/3rd-place \
   -w /solutions/3rd-place \
   $IMAGE bash -c "$SWACMD > swa$FOLD.out"

###########################################
###  Computing Similarities
read -r -d '' SIMCMD << EOM
mkdir -p similarities; \
CUDA_VISIBLE_DEVICES=$DEV python3 inference_similarity.py \
  --config=configs/test$FOLD.yml \
  --tta_landmark=0 \
  --checkpoint_name=swa.pth \
  --output_path=similarities/test$FOLD.csv
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_3rd \
   -v $(pwd)/data:/solutions/3rd-place/data \
   -v $CHECKPOINT_PATH/3rd-place/train_logs:/solutions/3rd-place/train_logs \
   -v $(pwd)/solutions/3rd-place:/solutions/3rd-place \
   -w /solutions/3rd-place \
   $IMAGE bash -c "$SIMCMD > sim$FOLD.out"

###########################################
### Generating Predictions
read -r -d '' PREDCMD << EOM
CUDA_VISIBLE_DEVICES=$DEV python3 make_submission.py \
  --threshold=0.385 \
  --input_path=similarities/test$FOLD.csv \
  --sample_path=data/test$FOLD.sample.csv \
  --output_path=results/test$FOLD.csv
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_3rd \
   -v $(pwd)/data:/solutions/3rd-place/data \
   -v $CHECKPOINT_PATH/3rd-place/train_logs:/solutions/3rd-place/train_logs \
   -v $(pwd)/solutions/3rd-place:/solutions/3rd-place \
   -w /solutions/3rd-place \
   $IMAGE bash -c "$PREDCMD > pred$FOLD.out"

###########################################
### MAP
read -r -d '' MAPCMD << EOM
CUDA_VISIBLE_DEVICES=$DEV python3 util/test/test.py \
    --name "Test #$FOLD" \
    --solution "3rd solution" \
    --description "DenseNet-121 trained 300 epochs" \
    --classes test/sets/classes.csv \
    --test test/new-sets/test\#$FOLD/test.csv \
    --train test/new-sets/test\#$FOLD/train.csv \
    --prediction solutions/3rd-place/results/test$FOLD.csv \
    --report-output solutions/3rd-place/results/test$FOLD.md
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_3rd \
   -v $(pwd)/data:/solutions/3rd-place/data \
   -v $(pwd)/solutions/3rd-place:/solutions/3rd-place \
   -w /solutions/3rd-place \
   $IMAGE bash -c "$MAPCMD > map$FOLD.out"
