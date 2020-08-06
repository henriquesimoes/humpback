#!/bin/bash

thres=0.385

for i in 1 2; do
  echo "Inferencing test #$i"; echo
  echo "Start time: $(date "+%Y-%m-%d %H:%M:%S")"

  if [ ! -f train_logs/test$i/checkpoint/swa.pth ]; then
    echo "Start weight averaging models from test #$i dataset"
    CUDA_VISIBLE_DEVICES=0 python swa.py --config configs/test$i.yml
    if [ $? -ne 0 ]; then break; fi
  fi

  echo "Inference similarities for test #$i"
  CUDA_VISIBLE_DEVICES=0 python inference_similarity.py --config=configs/test$i.yml --output_path=similarities/test$i.csv --checkpoint_name=swa.pth --tta_landmark=0
  if [ $? -ne 0 ]; then break; fi
  
  echo "Packing predictions in a CSV file"
  python3 make_submission.py --input_path=similarities/test$i.csv --output_path=results/test$i.csv --sample_path=data/test$i.sample.csv --threshold=$thres
  if [ $? -ne 0 ]; then break; fi
  
  echo "End time: $(date "+%Y-%m-%d %H:%M:%S")"
done
