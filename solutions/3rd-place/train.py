from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import math
import argparse
import pprint
from collections import defaultdict

import torch
import torch.nn.functional as F

from datasets import get_dataloader
from transforms import get_transform
from tasks import get_task
from optimizers import get_optimizer
from schedulers import get_scheduler
import utils
import utils.config
import utils.checkpoint
import utils.log

def evaluate_single_epoch(config, task, dataloader, epoch,
                          writer):
    task.get_model().eval()
    cal_metric_once = config.eval.cal_metric_once

    log_dict = {'mode': 'eval'}
    with torch.no_grad():
        batch_size = config.eval.batch_size
        total_size = len(dataloader.dataset)
        total_step = math.ceil(total_size / batch_size)

        loss_list = []
        metric_list_dict = defaultdict(list)
        data_list_dict = defaultdict(list)
        for i, data in enumerate(dataloader):
            images = data['image'].cuda()
            labels = data['label'].cuda()

            outputs = task.forward(images=images)
            loss = task.loss(outputs, labels)
            loss_list.append(loss.item())

            predicts = task.inference(outputs=outputs)
            if cal_metric_once:
                for key, value in predicts.items():
                    data_list_dict[key].extend(value.cpu().numpy())
                for key, value in data.items():
                    if key == 'image':
                        continue
                    data_list_dict[key + 's'].extend(value)
            else:
                metric_dict = task.metrics(labels=labels, **predicts, **data)
                for key, value in metric_dict.items():
                    metric_list_dict[key].append(value)

        log_dict['loss'] = sum(loss_list) / len(loss_list)

        if cal_metric_once:
            metric_dict = task.metrics(**data_list_dict)
            log_dict.update(metric_dict)
        else:
            for key, values in metric_list_dict.items():
                log_dict[key] = sum(values) / len(values)

        writer.step(log_dict)

        return log_dict['score']


def train_single_epoch(config, task, dataloader, optimizer,
                       epoch, writer):
    task.get_model().train()

    batch_size = config.train.batch_size
    total_size = len(dataloader.dataset)
    total_step = total_size // batch_size

    log_dict = {'mode': 'train'}
    for i, data in enumerate(dataloader):
        images = data['image'].cuda()
        labels = data['label'].cuda()
        outputs = task.forward(images=images, labels=labels)
        loss = task.loss(outputs, labels)
        log_dict['loss'] = loss.item()

        predicts = task.inference(outputs=outputs, labels=labels)
        metric_dict = task.metrics(labels=labels, **predicts)
        log_dict.update(metric_dict)

        loss.backward()

        warmup = True
        if warmup and epoch < 3:
            if (i+1) % 2 == 0:
                optimizer.step()
                optimizer.zero_grad()
        else:
            if config.train.num_grad_acc is None:
                optimizer.step()
                optimizer.zero_grad()
            elif (i+1) % config.train.num_grad_acc == 0:
                optimizer.step()
                optimizer.zero_grad()

        f_epoch = epoch + i / total_step

        log_dict['lr'] = optimizer.param_groups[0]['lr']

        log_dict['epoch'] = f_epoch
        log_dict['iter'] = epoch * total_size + i

        writer.step(log_dict)

def train(config, task, dataloaders, optimizer, scheduler, writer, start_epoch):
    scores = []
    best_score = 0.0
    best_score_mavg = 0.0

    writer.start()
    for epoch in range(start_epoch, config.train.num_epochs):
        # train phase
        train_single_epoch(config, task, dataloaders['train'],
                           optimizer, epoch, writer)

        # val phase
        score = evaluate_single_epoch(config, task, dataloaders['dev'],
                                      epoch, writer)
        scores.append(score)

        if config.scheduler.name == 'reduce_lr_on_plateau':
          scheduler.step(score)
        elif config.scheduler.name != 'reduce_lr_on_plateau':
          scheduler.step()

        if epoch % config.train.save_checkpoint_epoch == 0:
            utils.checkpoint.save_checkpoint(config, task.get_model(), optimizer,
                                             epoch, 0, keep=10)

        scores = scores[-20:]
        score_mavg = sum(scores) / len(scores)
        writer.write(f'Mean average on {epoch} of the last 20 points: {score_mavg}')
        if score > best_score:
            best_score = score
            writer.write(f'New best MAP@5 found on epoch {epoch}: {best_score}')
            utils.checkpoint.save_checkpoint(config, task.get_model(), optimizer,
                                             epoch, keep=10, name='best.score')
            utils.checkpoint.copy_last_n_checkpoints(config, 10, 'best.score.{:04d}.pth')

        if score_mavg > best_score_mavg:
            best_score_mavg = score_mavg
            writer.write(f'New best average MAP@5 found on epoch {epoch}: {best_score_mavg}')
            utils.checkpoint.save_checkpoint(config, task.get_model(), optimizer,
                                             epoch, keep=10, name='best.score_mavg')
            utils.checkpoint.copy_last_n_checkpoints(config, 10, 'best.score_mavg.{:04d}.pth')

    return {'score': best_score, 'score_mavg': best_score_mavg}

def run(config, writer):
    train_dir = config.train.dir

    task = get_task(config)
    optimizer = get_optimizer(config, task.get_model().parameters())

    checkpoint = utils.checkpoint.get_initial_checkpoint(config)
    if checkpoint is not None:
        last_epoch, step = utils.checkpoint.load_checkpoint(task.get_model(),
                                                            optimizer,
                                                            checkpoint)
    else:
        last_epoch, step = -1, -1

    writer.write('Training from checkpoint: {}, last epoch:{}'.format(checkpoint, last_epoch))
    scheduler = get_scheduler(config, optimizer, last_epoch)

    preprocess_opt = task.get_preprocess_opt()
    dataloaders = {split:get_dataloader(config, split,
                                        get_transform(config, split,
                                                      **preprocess_opt))
                   for split in ['train', 'dev']}

    score = train(config, task, dataloaders, optimizer, scheduler,
          writer, last_epoch+1)

    writer.write('Best score: {:0.5f}\nBest average score: {:.5f}\n'.format(score['score'], score['score_mavg']))

def parse_args():
    description = 'Train humpback whale identification'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--config', dest='config_file',
                        help='configuration filename',
                        default=None, type=str)
    return parser.parse_args()

def main():
    import warnings
    warnings.filterwarnings("ignore")

    args = parse_args()
    if args.config_file is None:
      raise Exception('no configuration file')

    config = utils.config.load(args.config_file)
    utils.prepare_train_directories(config)

    writer = utils.log.Writer(config.train.dir, log_step=config.train.log_step)

    writer.write('Train humpback whale identification')
    writer.write('Configuration: ')
    writer.write(pprint.PrettyPrinter(indent=2).pformat(config))

    run(config, writer)

    writer.close()

if __name__ == '__main__':
    main()
