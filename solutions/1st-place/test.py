import pandas as pd
import numpy as np
import os
import torch
from tqdm import tqdm
from models import *
from dataSet import *
import os
import shutil
import datetime
# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
num_TTA = 2


def train_collate(batch):

    batch_size = len(batch)
    images = [
    ]
    names = []
    for b in range(batch_size):
        if batch[b][0] is None:
            continue
        else:
            images.extend(batch[b][0])
            names.append(batch[b][1])
    images = torch.stack(images, 0)
    return images, names


def transform(image, mask):
    raw_iamge = cv2.resize(image, (512, 256))
    raw_mask = cv2.resize(mask, (512, 256))
    raw_mask = raw_mask[:, :, None]
    raw_iamge = np.concatenate([raw_iamge, raw_mask], 2)
    images = []

    image = raw_iamge.copy()
    image = np.transpose(image, (2, 0, 1))
    image = image.copy().astype(np.float)
    image = torch.from_numpy(image).div(255).float()
    images.append(image)

    image = raw_iamge.copy()
    image = np.fliplr(image)
    image = np.transpose(image, (2, 0, 1))
    image = image.copy().astype(np.float)
    image = torch.from_numpy(image).div(255).float()
    images.append(image)

    return images



def test(checkPoint_start=0, fold_index=1, model_name='senet154', num_classes=5004):
    names_test = os.listdir('./input/test')
    batch_size = 16
    dst_test = WhaleTestDataset(names_test, mode='test', transform=transform)
    dataloader_test = DataLoader(dst_test, batch_size=batch_size, num_workers=8, collate_fn=train_collate)
    label_id = dst_test.labels_dict
    id_label = {v:k for k, v in label_id.items()}
    id_label[num_classes] = 'new_whale'
    model = model_whale(num_classes=num_classes * 2, inchannels=4, model_name=model_name).cuda()
    resultDir = './result/{}_{}'.format(model_name, fold_index)
    checkPoint = os.path.join(resultDir, 'checkpoint')

    # npy_dir = resultDir + '/out_{}'.format(checkPoint_start)
    # os.makedirs(npy_dir, exist_ok=True)
    if not checkPoint_start == 0:
        model.load_pretrain(os.path.join(checkPoint, '%08d_model.pth' % (checkPoint_start)),skip=[])
        ckp = torch.load(os.path.join(checkPoint, '%08d_optimizer.pth' % (checkPoint_start)))
        best_t = ckp['best_t']
        print('best_t:', best_t)
    labelstrs = []
    allnames = []

    log = open(os.path.join(resultDir, 'inference.log'), mode='w')
    log.write('Inference start time: {} \n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    with torch.no_grad():
        model.eval()
        for data in tqdm(dataloader_test):
            images, names = data
            images = images.cuda()
            _, _, outs = model(images)
            outs = torch.sigmoid(outs)
            outs_zero = (outs[::2, :num_classes] + outs[1::2, num_classes:])/2
            outs = outs_zero
            for out, name in zip(outs, names):
                out = torch.cat([out, torch.ones(1).cuda()*best_t], 0)
                out = out.data.cpu().numpy()
                # np.save(os.path.join(npy_dir, '{}.npy'.format(name)), out)
                top5 = out.argsort()[-5:][::-1]
                str_top5 = ''
                for t in top5:
                    str_top5 += '{} '.format(id_label[t])
                str_top5 = str_top5[:-1]
                allnames.append(name)
                labelstrs.append(str_top5)

    pd.DataFrame({'Image': allnames,'Id': labelstrs}).to_csv('test_{}_sub_fold{}.csv'.format(model_name, fold_index), index=None)

    log.write('Inference end time: {} \n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    log.close()

if __name__ == '__main__':

    model_name = 'senet154'

    ### Kaggle
    # num_classes = 5004
    ## First submission
    # checkPoint_start = 67200
    # fold_index = 1
    #
    ## Second submission
    # checkPoint_start = 71000
    # fold_index = 2
    #
    ### Our tests
    # num_classes = 4887
    ## Test #1 inference
    # checkPoint_start = 57200
    # fold_index = 6
    #
    ## Test #2 inference
    # checkPoint_start = 106600
    # fold_index = 7

    test(checkPoint_start, fold_index, model_name, num_classes)

