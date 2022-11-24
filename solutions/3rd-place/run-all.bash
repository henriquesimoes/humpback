#!/bin/bash

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
ln -s data/train data/test
 
###########################################
### TRAIN
read -r -d '' TRAINCMD << EOM
CUDA_VISIBLE_DEVICES=0,1,2 python3 train.py \
   --config==configs/test$FOLD.yml
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_3rd \
   -v $(pwd)/data:/solutions/3rd-place/data \
   -v $CHECKPOINT_PATH/3rd-place/train_logs:/solutions/3rd-place/train_logs \
   -v $(pwd)/solutions/3rd-place:/solutions/3rd-place \
   -w /solutions/3rd-place \
   ufoym/deepo:all-py38-cu113 bash -c "$TRAINCMD > train$FOLD.out"

###########################################
### TEST
read -r -d '' TESTCMD << EOM
CUDA_VISIBLE_DEVICES=$DEV python main.py \
  --mode=test \
  --fold_index=$FOLD \
  --batch_size=32 \
  --pretrained_model=max_valid_model.pth
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_2nd \
   -v $(pwd)/data:/dataset \
   -v $CHECKPOINT_PATH:/solutions/2nd-place/models \
   -v $(pwd)/solutions/2nd-place:/solutions/2nd-place \
   -w /solutions/2nd-place \
   humpback2 bash -c "$TESTCMD > test$FOLD.out"

###########################################
### ENSEMBLE
read -r -d '' ENSMLCMD << EOM
CUDA_VISIBLE_DEVICES=$DEV python ensemble.py \
  --name=resnet101_test${FOLD}_256_512
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_2nd \
   -v $(pwd)/data:/dataset \
   -v $CHECKPOINT_PATH:/solutions/2nd-place/models \
   -v $(pwd)/solutions/2nd-place:/solutions/2nd-place \
   -w /solutions/2nd-place \
   humpback2 bash -c "$ENSMLCMD > ensml$FOLD.out"

### Change result name
mv $HUMP/solutions/2nd-place/result.csv  $HUMP/solutions/2nd-place/result$FOLD.csv 

###########################################
### MAP
read -r -d '' MAPCMD << EOM
CUDA_VISIBLE_DEVICES=$DEV python3 util/test/test.py \
    --name "Test #$FOLD" \
    --solution "2nd solution" \
    --description "ResNet-101 (512x256) trained 100 epochs" \
    --classes test/sets/classes.csv \
    --test test/new-sets/test\#$FOLD/test.csv \
    --train test/new-sets/test\#$FOLD/train.csv \
    --prediction solutions/2nd-place/result$FOLD.csv \
    --report-output solutions/2nd-place/test$FOLD.md
EOM

docker run --rm \
   --shm-size=8GB \
   --runtime=nvidia --gpus all \
   --name humpback_2nd \
   -v $(pwd)/data:/dataset \
   -v $(pwd):/solutions/2nd-place \
   -w /solutions/2nd-place \
   humpback2 bash -c "$MAPCMD > map$FOLD.out"
