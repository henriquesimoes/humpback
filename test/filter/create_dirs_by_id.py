import os, subprocess
import pandas as pd
import argparse
from collections import defaultdict
from tqdm import tqdm

def get_config():
  ap = argparse.ArgumentParser()
  
  ap.add_argument("--labels", required=True, help="Train labels")
  ap.add_argument("--data", required=True, help="Train dataset folder")
  ap.add_argument("--duplicates", default=None, help="Duplicates CSV file")
  ap.add_argument("--append-id", type=bool, dest="append_id", default=False, help="Append original id to filenames")
  ap.add_argument("--output", default="output", help="Output folder")
  ap.add_argument("--not-new", dest="not_new", required=True, help="Not new whale CSV file")
  ap.add_argument("--ignore", default=None, help="Classes to ignore CSV file")
  ap.add_argument("--merge-one-shot", type=bool, default=False, dest="merge_one_shot", help="Aggregate one shot classes into a single folder")

  return ap.parse_args()

def merge_duplicates(label_df, duplicate_df):
  id_dict = {}

  if duplicate_df is not None:
    for key, row in duplicate_df.iterrows():
      duplicates = row["Duplicates"].split()
      representant = duplicates[0]
      
      for duplicate in duplicates:
        id_dict[duplicate] = representant
  
  result = {}
  for image, row in label_df.iterrows():
    id = row['Id']
    if id not in id_dict:
      id_dict[id] = id

    result[image] = id_dict[id]
  
  return result

def merge_not_new(id_dict, not_new_df):
  for image, row in not_new_df.iterrows():
    id_dict[image] = row['Id']
  
  return id_dict

def get_ignore_set(config):
  ignore_set = set()

  if config.ignore:
    ignore_df = pd.read_csv(config.ignore)

    for id in ignore_df.to_dict('list')['Id']:
      ignore_set.add(id)

  return ignore_set

def get_one_shot_set(config, id_dict):
  images = set()

  if config.merge_one_shot:
    images_dict = defaultdict(list)

    for image, id in id_dict.items():
      images_dict[id].append(image)

    for id in images_dict.keys():
      if len(images_dict[id]) == 1:
        images.add(images_dict[id][0])

  return images

def main():
  config = get_config()

  duplicate_df = pd.read_csv(config.duplicates) if config.duplicates is not None else None
  label_df = pd.read_csv(config.labels).set_index('Image')
  not_new_df = pd.read_csv(config.not_new).set_index('Image')

  id_dict = merge_duplicates(label_df, duplicate_df)
  id_dict = merge_not_new(id_dict, not_new_df)

  ignore_set = get_ignore_set(config)
  one_shot_set = get_one_shot_set(config, id_dict)

  log = open('ln.log', 'w')

  for image, row in tqdm(label_df.iterrows(), total=len(label_df)):
    origin = os.path.join(config.data, image)

    if id_dict[image] in ignore_set:
      continue

    dest_name = "one-shot" if image in one_shot_set else id_dict[image]

    destination = os.path.join(config.output, dest_name)
    os.makedirs(destination, exist_ok=True)

    name = row["Id"] + "." + image if config.append_id else image
    command = "ln -s ../../" + origin + " " + name

    process = subprocess.Popen(command.split(), cwd=destination, stderr=log)

    out, error = process.communicate()
    if error is not None:
      break

if __name__ == "__main__":
  main()
