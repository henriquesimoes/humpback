import os
import argparse

from utils import *
from process.data import *
from process.triplet_sampler import *
from loss.loss import  softmax_loss, TripletLoss, focal_OHEM

whale_id_num = 4887
class_num = whale_id_num * 2

def get_model(model, config):

    if model == 'resnet101':
        from net.model_resnet101 import Net
    elif model == 'seresnet101':
        from net.model_seresnet101 import Net
    elif model == 'seresnext101':
        from net.model_seresnext101 import Net

    net = Net(num_class=class_num, s1 = config.s1 , m1 = config.m1, s2 = config.s2)
    return net

def do_valid(net, valid_loader, hard_ratio, is_flip = False):
    valid_num  = 0
    truths   = []
    losses   = []

    probs = []
    labels = []

    with torch.no_grad():
        for input, truth_, _ in valid_loader:
            truth = torch.FloatTensor(len(truth_), class_num+1)
            truth.zero_()
            truth.scatter_(1, truth_.view(-1,1), 1)
            truth = truth[:,:class_num]

            input = input.cuda()
            truth = truth.cuda()

            input = to_var(input)
            truth = to_var(truth)
            truth_ = to_var(truth_)

            logit, _, feas = net(input, label = None, is_infer = True)
            loss = focal_OHEM(logit, truth_, truth, hard_ratio)

            prob = torch.sigmoid(logit)
            prob  = prob.data.cpu().numpy()
            label = truth_.data.cpu().numpy()

            if is_flip:
                prob = prob[:, whale_id_num:]
                label -= whale_id_num
            else:
                prob = prob[:,:whale_id_num]
                label[label==class_num] = whale_id_num

            probs.append(prob)
            labels.append(label)
            valid_num += len(input)

            loss_tmp = loss.data.cpu().numpy().reshape([1])
            losses.append(loss_tmp)
            truths.append(truth.data.cpu().numpy())

    assert (valid_num == len(valid_loader.sampler))
    # ------------------------------------------------------
    loss = np.concatenate(losses,axis=0)
    loss = loss.mean()

    prob = np.concatenate(probs)
    label = np.concatenate(labels)

    threshold = np.arange(0.0, 1.0, 0.02)
    max_p = 0.0
    max_thres = 0.0
    top_final = (0, 0)

    for thres in threshold:
        precision, top = metric(prob, label, thres=thres)
        if precision > max_p:
            max_p = precision
            max_thres = thres
            top_final = top

    print('maximum MAP@5={:.5f} reached with new-whale threshold={:0.2f}'.format(max_p, max_thres))
    valid_loss = np.array([loss, top_final[0], top_final[1], max_p])
    return valid_loss, max_thres

def run_train(config):
    base_lr = 30e-5

    def adjust_lr_and_hard_ratio(optimizer, ep):
        if ep < 10:
            lr = 1e-4 * (ep // 5 + 1)
            hard_ratio = 1 * 1e-2
        elif ep < 40:
            lr = 3e-4
            hard_ratio = 7 * 1e-3
        elif ep < 50:
            lr = 1e-4
            hard_ratio = 6 * 1e-3
        elif ep < 60:
            lr = 5e-5
            hard_ratio = 5 * 1e-3
        else:
            lr = 1e-5
            hard_ratio = 4 * 1e-3
        for p in optimizer.param_groups:
            p['lr'] = lr
        return lr, hard_ratio

    batch_size = config.batch_size
    image_size = (config.image_h, config.image_w)
    NUM_INSTANCE = 4

    ## setup  -----------------------------------------------------------------------------
    if config.is_pseudo:
        config.model_name = config.model + '_test' + str(config.fold_index) + '_pseudo'\
                            '_' + str(config.image_h) + '_' + str(config.image_w)
    else:
        config.model_name = config.model + '_test' + str(config.fold_index) + \
                            '_'+str(config.image_h)+ '_'+str(config.image_w)

    out_dir = os.path.join('./models/', config.model_name)

    os.makedirs(os.path.join(out_dir,'checkpoint'), exist_ok=True)

    if config.pretrained_model is not None:
        initial_checkpoint = os.path.join(out_dir, 'checkpoint', config.pretrained_model)
    else:
        initial_checkpoint = None

    train_dataset = WhaleDataset('train', test_index=config.fold_index, image_size=image_size,is_pseudo=config.is_pseudo)

    train_list = WhaleDataset('train_list', test_index=config.fold_index, image_size=image_size, is_pseudo=config.is_pseudo)

    valid_dataset = WhaleDataset('val', test_index=config.fold_index, image_size=image_size, augment=[0.0], is_flip=False)

    valid_loader  = DataLoader(valid_dataset,
                               shuffle = False,
                               batch_size  = batch_size,
                               drop_last   = False,
                               num_workers = 16,
                               pin_memory  = True)

    valid_dataset_flip = WhaleDataset('val', test_index=config.fold_index, image_size=image_size, augment=[0.0], is_flip=True)

    valid_loader_flip  = DataLoader(valid_dataset_flip,
                                    shuffle = False,
                                    batch_size  = batch_size,
                                    drop_last   = False,
                                    num_workers = 16,
                                    pin_memory  = True)

    net = get_model(config.model, config)
    ##-----------------------------------------------------------------------------------------------------------
    if 1:
        for p in net.basemodel.layer0.parameters(): p.requires_grad = False
        for p in net.basemodel.layer1.parameters(): p.requires_grad = False

    net = torch.nn.DataParallel(net)
    print(net)
    net = net.cuda()

    log = open(out_dir+'/log.train.txt', mode='a')
    log.write('Training start time: {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    log.write('\t__file__     = %s\n' % __file__)
    log.write('\tout_dir      = %s\n' % out_dir)
    log.write('\n')

    ##-----------------------------------------------------------------------------------------------------------
    log.write('** dataset setting **\n')
    assert(len(train_dataset)>=batch_size)
    log.write('batch_size = %d\n'%(batch_size))
    log.write('train_dataset : %d\n'%(len(train_dataset)))
    log.write('valid_dataset : %d\n'%(len(valid_dataset)))
    log.write('\n')

    ## net ----------------------------------------
    log.write('** net setting **\n')
    if initial_checkpoint is not None:
        log.write('\tinitial_checkpoint = %s\n' % initial_checkpoint)
        net.load_state_dict(torch.load(initial_checkpoint, map_location=lambda storage, loc: storage))
        print('\tinitial_checkpoint = %s\n' % initial_checkpoint)

    log.write('%s\n\n'%(net))

    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, net.parameters()),
                                 lr=base_lr,
                                 betas=(0.9, 0.999),
                                 eps=1e-08,
                                 weight_decay=0.0002)

    iter_smooth = 50
    start_iter = 0

    log.write('\n')
    valid_loss   = np.zeros(6,np.float32)
    batch_loss   = np.zeros(6,np.float32)
    train_loss   = np.zeros(6,np.float32)
    valid_thres  = 0.5

    i    = 0
    start = timer()
    max_valid = 0

    for epoch in range(config.train_epoch):
        sum_train_loss = np.zeros(6, np.float32)
        sum = 0
        optimizer.zero_grad()

        rate, hard_ratio = adjust_lr_and_hard_ratio(optimizer, epoch + 1)

        print('change lr: '+str(rate))
        print('change hard_ratio: ' + str(hard_ratio))
        log.write('change hard_ratio: ' + str(hard_ratio))
        log.write('\n')

        train_loader = DataLoader(train_dataset,
                                  sampler = WhaleRandomIdentitySampler(train_list,
                                                                     batch_size,
                                                                     NUM_INSTANCE,
                                                                     NW_ratio=0.25),
                                  batch_size=batch_size,
                                  drop_last=False,
                                  num_workers=16,
                                  pin_memory=True)
        header = '  lr      iter   epoch   |  val_loss  Top@1  Top@5  MAP@5  thres  | train_loss  Top@1  Top@5  MAP@5    |  batch_loss  Top@1   Top@5   MAP@5   |     Time\n' + \
                '-' * 170
        print(header)
        log.write(header + '\n')

        for input, truth_ , truth_NW_binary in train_loader:
            truth = torch.FloatTensor(len(truth_),class_num+1)
            truth.zero_()
            truth.scatter_(1,truth_.view(-1,1),1)
            truth = truth[:, :class_num]
            iter = i + start_iter

            # one iteration update  -------------
            net.train()
            input = input.cuda()
            truth = truth.cuda()
            truth_ = truth_.cuda()

            input = to_var(input)
            truth = to_var(truth)
            truth_ = to_var(truth_)

            logit, logit_softmax, feas = net.forward(input, label = truth_, is_infer = True)

            truth_NW_binary = truth_NW_binary.cuda()
            truth_NW_binary = to_var(truth_NW_binary)
            indexs_NoNew = (truth_NW_binary != 1).nonzero().view(-1)
            indexs_New = (truth_NW_binary == 1).nonzero().view(-1)

            loss_focal = focal_OHEM(logit, truth_,truth, hard_ratio)* config.focal_w
            loss_softmax = softmax_loss(logit_softmax[indexs_NoNew], truth_[indexs_NoNew]) * config.softmax_w
            loss_triplet = TripletLoss(margin=0.3)(feas, truth_) * config.triplet_w

            loss = loss_focal + loss_softmax + loss_triplet

            prob = torch.sigmoid(logit)

            prob = prob.data.cpu().numpy()
            truth_ = truth_.data.cpu().numpy()

            precision, top = metric(prob, truth_, thres=valid_thres)
            top1, top5 = top

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            batch_loss[:4] = np.array((loss.data.cpu().numpy(),
                                       top1,
                                       top5,
                                       precision)).reshape([4])

            sum_train_loss += batch_loss
            sum += 1

            if iter % iter_smooth == 0:
                train_loss = sum_train_loss / sum
                sum_train_loss = np.zeros(6, np.float32)
                sum = 0

            stats = '%0.7f  %5.2f k  %3d | %5.3f  %7.3f  %7.3f   %0.3f   %0.2f  | %5.3f  %7.3f  %7.3f   %0.3f   | %5.3f   %7.3f  %7.3f   %0.3f   | %s' % (\
                             rate, iter / 1000.0, epoch,
                             valid_loss[0], valid_loss[1], valid_loss[2], valid_loss[3], valid_thres,
                             train_loss[0], train_loss[1], train_loss[2], train_loss[3],
                             batch_loss[0], batch_loss[1], batch_loss[2], batch_loss[3],
                             time_to_str((timer() - start),'min'))

            if i % 10 == 0:
                print(stats)
            if i % 200 == 0:
                log.write(stats + '\n')

            i = i + 1

            if iter > start_iter and (i % 200 == 0):
                net.eval()
                valid_loss, valid_thres = do_valid(net, valid_loader, hard_ratio, is_flip=False)
                valid_loss_flip, valid_thres_flip = do_valid(net, valid_loader_flip, hard_ratio, is_flip=True)
                valid_loss, valid_thres = (valid_loss + valid_loss_flip) / 2.0, (valid_thres + valid_thres_flip) / 2.0
                net.train()

                if max_valid < valid_loss[3] and (epoch + 1) > 40:
                    max_valid = valid_loss[3]
                    saving_msg = f'New maximum MAP@5 reached on {iter}th iteration (epoch {epoch}): {max_valid}... saving on disk.'
                    print(saving_msg)
                    log.write(saving_msg + '\n')

                    torch.save(net.state_dict(), out_dir + '/checkpoint/max_valid_model.pth')

        if (epoch+1) % config.iter_save_interval == 0 and epoch>0:
            torch.save(net.state_dict(), out_dir + '/checkpoint/%08d_model.pth' % (epoch))

        net.eval()
        valid_loss, valid_thres = do_valid(net, valid_loader, hard_ratio, is_flip=False)
        valid_loss_flip, valid_thres_flip = do_valid(net, valid_loader_flip, hard_ratio, is_flip=True)
        valid_loss, valid_thres = (valid_loss + valid_loss_flip) / 2.0, (valid_thres + valid_thres_flip) / 2.0
        net.train()

        if max_valid < valid_loss[3]:
            max_valid = valid_loss[3]
            saving_msg = f'New maximum MAP@5 reached on {iter}th iteration (epoch {epoch}): {max_valid}... saving on disk.'

            print(saving_msg)
            log.write(saving_msg + '\n')

            torch.save(net.state_dict(), out_dir + '/checkpoint/max_valid_model.pth')

    log.write('\nTraining end time: {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    log.close()

def run_infer(config):
    batch_size = config.batch_size
    image_size = (config.image_h, config.image_w)

    ## setup  -----------------------------------------------------------------------------
    if config.is_pseudo:
        config.model_name = config.model + '_test' + str(config.fold_index) + '_pseudo'\
                            '_' + str(config.image_h) + '_' + str(config.image_w)
    else:
        config.model_name = config.model + '_test' + str(config.fold_index) + \
                            '_'+str(config.image_h)+ '_'+str(config.image_w)

    out_dir = os.path.join('./models/', config.model_name)

    net = get_model(config.model, config)
    net = torch.nn.DataParallel(net)
    print(net)

    if config.pretrained_model is not None:
        initial_checkpoint = os.path.join(out_dir, 'checkpoint', config.pretrained_model)
    else:
        initial_checkpoint = None

    if initial_checkpoint is not None:
        print(initial_checkpoint)
        net.load_state_dict(torch.load(initial_checkpoint, map_location=lambda storage, loc: storage))


    net = net.cuda()
    net.eval()

    valid_dataset = WhaleDataset('val', test_index=config.fold_index,
                                 image_size=image_size,
                                 augment=[0.0],
                                 is_flip=False)

    valid_loader  = DataLoader(valid_dataset,
                               shuffle=False,
                               batch_size  = batch_size,
                               drop_last   = False,
                               num_workers = 8,
                               pin_memory  = True)

    valid_dataset_flip = WhaleDataset('val', test_index=config.fold_index, image_size=image_size,
                                      augment=[0.0],
                                      is_flip=True)

    valid_loader_flip = DataLoader(valid_dataset_flip,
                                   shuffle=False,
                                   batch_size=batch_size,
                                   drop_last=False,
                                   num_workers=8,
                                   pin_memory=True)

    print('          loss    Top@1    Top@5    MAP@5   threshold')
    valid_loss, thres = do_valid(net, valid_loader,  hard_ratio= 1 * 1e-2, is_flip=False)
    print('original: %0.5f  %0.5f  %0.5f  %0.5f  %0.2f' % ( valid_loss[0], valid_loss[1], valid_loss[2], valid_loss[3], thres))

    valid_loss, thres = do_valid(net, valid_loader_flip,  hard_ratio= 1 * 1e-2, is_flip=True)
    print('flipped:  %0.5f  %0.5f  %0.5f  %0.5f  %0.2f' % (valid_loss[0], valid_loss[1], valid_loss[2], valid_loss[3], thres))

    # 2TTA
    augments = [[0.0],[1.0]]
    print('TTAs:\n', augments)

    log = open(os.path.join(out_dir, 'inference.log'), 'w')
    log.write('Inference start time: {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    for index in range(len(augments)):
        print(augments[index])
        infer_dataset = WhaleDataset('test', test_index=config.fold_index, image_size = image_size,augment=augments[index])
        infer_loader  = DataLoader(infer_dataset,
                                   shuffle=False,
                                   batch_size  = batch_size,
                                   drop_last   = False,
                                   num_workers = 8,
                                   pin_memory  = True)

        # infer test
        test_ids = []
        probs = []
        from tqdm import tqdm
        for i,(id, input) in enumerate(tqdm(infer_loader)):
            test_ids += id
            input = input.cuda()
            input = to_var(input)
            logit, _, fea = net.forward(input, None, is_infer=True)
            prob = F.sigmoid(logit)

            if augments[index][0] == 0.0:
                prob = prob[:, :whale_id_num]
            elif augments[index][0] == 1.0:
                prob = prob[:, whale_id_num:]

            probs += prob.data.cpu().numpy().tolist()
        if initial_checkpoint is not None:
            save_path = initial_checkpoint.replace('.pth','')
        else:
        	save_path='./save_submission'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        save_path = os.path.join(save_path, '2TTA_' + str(index))
        print(save_path+'.csv')
        prob_to_csv_top5(probs, test_ids, save_path)

    log.write('Inference end time: {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    log.close()

def main(config):
    if config.mode == 'train':
        run_train(config)

    if config.mode == 'test':
        with torch.no_grad():
            run_infer(config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--fold_index', type=int, default=1)
    parser.add_argument('--model', type=str, default='resnet101')
    parser.add_argument('--batch_size', type=int, default=128)

    parser.add_argument('--image_h', type=int, default=256)
    parser.add_argument('--image_w', type=int, default=512)

    parser.add_argument('--s1', type=float, default=64.0)
    parser.add_argument('--m1', type=float, default=0.5)
    parser.add_argument('--s2', type=float, default=16.0)

    parser.add_argument('--focal_w', type=float, default=1.0)
    parser.add_argument('--softmax_w', type=float, default=0.1)
    parser.add_argument('--triplet_w', type=float, default=1.0)

    parser.add_argument('--is_pseudo', type=bool, default=False) # [Modified]: default=True

    parser.add_argument('--mode', type=str, default='train', choices=['train', 'val','val_fold','test_classifier','test','test_fold'])
    parser.add_argument('--pretrained_model', type=str, default=None)

    parser.add_argument('--iter_save_interval', type=int, default=5)
    parser.add_argument('--train_epoch', type=int, default=100)

    config = parser.parse_args()
    print(config)
    main(config)
