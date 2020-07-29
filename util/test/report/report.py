from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime

class Report():
  def __init__(self, dataset):
    self.date = datetime.now()
    self.dataset = dataset
    self.results = []
  
  def set_solution(self, solution):
    self.solution = solution

  def set_description(self, description):
    self.description = description

  def add_result(self, result):
    self.results.append(result)

  def __str__(self):
    out = "# Test Report\n\n"
    out += "## Configuration\n\n"
    if self.dataset:
      out += " - Dataset: " + self.dataset + "\n"
    if self.solution:
      out += " - Solution: " + str(self.solution) + "\n"
    if self.description:
      out += " - Description: " + self.description + "\n"
    out += " - Date: " + self.date.strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
    out += "## Test results: \n\n"

    for result in self.results:
      out += " - {}: {:10.5f}\n".format(result['metric'], result['result'])

    out += '\n'

    return out

class ReportManager:
  def __init__(self, dataset):
    self.dataset = dataset
    self._reset()

  def _reset(self):
    self.report = Report(self.dataset)

  def set_info(self, solution, description = ''):
    self.report.set_solution(solution)
    self.report.set_description(description)
  
  def add_metric(self, name, result):
    self.report.add_result({'metric': name, 'result': result})

  def finish(self, path, save=True):
    self.display()
    if save: self.save(path)
    self._reset()

  def save(self, path):
    f = open(path, 'w')
    f.write(str(self.report))
    f.close()

  def display(self):
    print(self.report, end='\n\n')
    