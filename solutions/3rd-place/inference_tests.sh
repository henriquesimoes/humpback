#!/bin/bash

set -e
export CUDA_VISIBLE_DEVICES=0

thres=0.385

for i in 1 2; do
  echo "Inferring test #$i"; echo
  echo "Start time: $(date "+%Y-%m-%d %H:%M:%S")"

  if [ ! -f train_logs/test$i/checkpoint/swa.pth ]; then
    echo "Start weight averaging models from test #$i dataset"
    python swa.py --config configs/test$i.yml
  fi

  echo "Infer similarities for test #$i"
  python inference_similarity.py \
    --config=configs/test$i.yml --output_path=similarities/test$i.csv --checkpoint_name=swa.pth --tta_landmark=0

  echo "Packing predictions in a CSV file"
  python3 make_submission.py --input_path=similarities/test$i.csv \
    --output_path=results/test$i.csv --sample_path=data/test$i.sample.csv --threshold=$thres

  echo "End time: $(date "+%Y-%m-%d %H:%M:%S")"
done
