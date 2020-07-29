from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import time
import os

class Writer:
  def __init__(self, log_dir, log_file='train.log', log_step=200, smooth_step=50):
    path = os.path.join(log_dir, log_file)
    self.file = open(path, mode='w')

    self.basic = {'lr': 0, 'iter': 0, 'epoch': 0}
    self.eval = {'loss': 0, 'map5': 0, 'top1': 0, 'top5': 0, 'thres': 0}
    self.batch = {'loss': 0, 'map5': 0, 'top1': 0, 'top5': 0}
    self.train = self.batch.copy()
    self.train_sum = self.train.copy()

    self.log_step = log_step
    self.smooth_step = smooth_step

    self.write("Training start time: {}".format(self._get_date()))
    self.header = '  lr         iter     epoch | ' + \
                ' val_loss    Top@1    Top@5    MAP@5 Threshold |' + \
                ' train_loss  Top@1    Top@5    MAP@5 |' + \
                ' batch_loss  Top@1    Top@5    MAP@5  |     Time  \n' + \
                '-' * 170
  
  def write(self, message):
    print(message)
    self.file.write(message + '\n')

  def start(self):
    self.start_time = time.time()
    self.write(self.header)

  def step(self, log_dict):
    assert 'mode' in log_dict

    if log_dict['mode'] == 'train':
      self._step_train(log_dict)
    elif log_dict['mode'] == 'eval':
      self._step_eval(log_dict)

    self._log_step()

  def close(self):
    self.write("Training end time: {}".format(self._get_date()))
    self.file.close()

  def _step_train(self, log_dict):
    for key in self.basic.keys():
      self.basic[key] = log_dict[key]
    
    for key in self.batch.keys():
      self.batch[key] = log_dict[key]
      self.train_sum[key] += log_dict[key]

    i = self.basic['iter']
    if i > 0 and i % self.smooth_step == 0:
      for key in self.train.keys():
        self.train[key] = self.train_sum[key] / self.smooth_step
        self.train_sum[key] = 0

  def _step_eval(self, log_dict):
    for key in self.eval.keys():
      self.eval[key] = log_dict[key]

  def _log_step(self):
    line  = " {:8.6f} {:7.2f} k {:6.2f}  |".format(self.basic['lr'], self.basic['iter'] / 1000.0, self.basic['epoch'])
    line += " {:8.4f} {:9.3f} {:8.3f} {:8.3f} {:8.2f}  | ".format(self.eval['loss'], self.eval['top1'], self.eval['top5'], self.eval['map5'], self.eval['thres'])
    line += " {:6.4f} {:9.3f} {:8.3f} {:8.3f} | ".format(self.train['loss'], self.train['top1'], self.train['top5'], self.train['map5'])
    line += " {:6.4f} {:9.3f} {:8.3f} {:8.3f}  | ".format(self.batch['loss'], self.batch['top1'], self.batch['top5'], self.batch['map5'])
    line += self._time_to_str(time.time() - self.start_time)

    if self.basic['iter'] % self.log_step == 0:
      self.write(line)
    else:
      print(line)

  def _get_date(self):
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  def _time_to_str(self, delta):
    delta /= 60
    return '%2d hr %02d min' % (delta // 60, delta % 60)

def test():
  import random

  writer = Writer('.')

  writer.start()
  for i in range(100):
    data = {'mode': 'train', 'lr': 1e-4, 'iter': i, 'epoch': i / 100}
    for k in writer.batch.keys():
      data[k] = random.random()
    writer.step(data)

  data = {'mode': 'eval'}
  for k in writer.eval.keys():
    data[k] = random.random()
  writer.step(data)

  for i in range(100, 200):
    data = {'mode': 'train', 'lr': 1e-4, 'iter': i, 'epoch': i / 100}
    for k in writer.batch.keys():
      data[k] = random.random()
    writer.step(data)

  writer.close()


if __name__ == "__main__":
  test()