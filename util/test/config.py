from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

def get_config():
  parser = argparse.ArgumentParser()

  parser.add_argument("--name", type=str, default=None, help="test name")

  parser.add_argument("--test", type=str, required=True, help="test ground truth labels")
  parser.add_argument("--train", type=str, required=True, help="train examples (CSV)")
  parser.add_argument("--prediction", type=str, required=True, help="prediction CSV file")

  parser.add_argument("--classes", type=str, required=True, help="list of available classes (CSV)")

  parser.add_argument("--solution", type=str, default=None, help="solution identification")
  parser.add_argument("--description", type=str, default=None, help="solution description")
  parser.add_argument("--report-output", type=str, dest="output", default="report.txt", help="report output file")

  parser.add_argument("--known-whale-only", type=bool, dest="known_only",
                      nargs='?', const=True, default=False,
                      help="use only known whales on evaluation")

  return parser.parse_args()
