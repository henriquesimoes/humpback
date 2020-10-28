python3 ../util/sets/create_sets.py \
  --labels ../data/train.csv \
  --remove filter/not_valid.csv \
  --hard filter/hard.csv,filter/texted.csv \
  --duplicate-images filter/duplicate_imgs.csv \
  --duplicate-classes filter/duplicates/duplicates.csv \
  --not-new filter/not_new.csv \
  --mislabeled filter/mislabeled.csv \
  --tests=2 \
  --test_percentage=0.2
