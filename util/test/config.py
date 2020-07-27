from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

def get_config():
  parser = argparse.ArgumentParser()

  parser.add_argument("--name", type=str, default="standard", help="test name")

  parser.add_argument("--test", type=str, required=True, help="test ground truth labels")
  parser.add_argument("--train", type=str, default=None, help="hard example relation (CSV)")
  parser.add_argument("--prediction", type=str, required=True, help="prediction CSV file")

  parser.add_argument("--classes", type=str, required=True, help="list of available classes (CSV)")

  parser.add_argument("--solution", type=str, required=True, help="solution identification")
  parser.add_argument("--description", type=str, default="", help="solution description")
  parser.add_argument("--report-output", type=str, dest="output", default="report.txt", help="report output file")

  return parser.parse_args()
