echo "Creating directories by id..."

python3 create_dirs_by_id.py \
  --labels ../../data/train.csv \
  --data ../../data/train \
  --duplicates duplicates/possible_duplicates.csv \
  --not-new not-new/possible_not_new.csv \
  --append-id=True \
  --merge-one-shot=True

echo "done."