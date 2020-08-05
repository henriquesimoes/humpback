#!/bin/bash

thres=0.385

for i in 1 2; do
  echo "Inferencing test #$i"

  python swa.py --config configs/test$1.yml
  CUDA_VISIBLE_DEVICES=0 python inference_similarity.py --config=configs/test$i.yml --output_path=similarities/test$i.csv --checkpoint_name=swa.pth --tta_landmark=0
  python3 make_submission.py --input_path=similarities/test$i.csv --output_path=results/test$i.csv --sample_path=data/test$i.sample.csv --threshold=$thres
done
