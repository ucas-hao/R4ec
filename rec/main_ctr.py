'''
-*- coding: utf-8 -*-
@File  : main_ctr.py
'''
# 1.python
import os
import time

import numpy as np
import json
import argparse
import datetime
# 2.pytorch
import torch
import torch.utils.data as Data
# 3.sklearn
from sklearn.metrics import roc_auc_score, log_loss

from utils import load_parse_from_json, setup_seed, load_data, weight_init, str2list
from models import DeepInterestNet, DCN, DeepFM, DIEN, xDeepFM, FiBiNet, FiGNN, AutoInt, GRU4REC, GRU4REC_movie
from dataset import AmzDataset
from optimization import AdamW, get_cosine_schedule_with_warmup, get_constant_schedule_with_warmup


def eval(model, test_loader):
    model.eval()
    losses = []
    preds = []
    labels = []
    t = time.time()
    with torch.no_grad():
        for batch, data in enumerate(test_loader):
            outputs = model(data)
            loss = outputs['loss']
            logits = outputs['logits']
            preds.extend(logits.detach().cpu().tolist())
            labels.extend(outputs['labels'].detach().cpu().tolist())
            losses.append(loss.item())
    eval_time = time.time() - t
    auc = roc_auc_score(y_true=labels, y_score=preds)
    ll = log_loss(y_true=labels, y_pred=preds)
    return auc, ll, np.mean(losses), eval_time


def test(args):
    model = torch.load(args.reload_path)
    test_set = AmzDataset(args.data_dir, 'test', args.task, args.max_hist_len, args.augment, args.aug_prefix)
    test_loader = Data.DataLoader(dataset=test_set, batch_size=args.batch_size, shuffle=False)
    print('Test data size:', len(test_set))
    auc, ll, loss, eval_time = eval(model, test_loader)
    print("test loss: %.5f, test time: %.5f, auc: %.5f, logloss: %.5f" % (loss, eval_time, auc, ll))


def load_model(args, dataset):
    algo = args.algo
    device = args.device
    if algo == 'DIN':
        model = DeepInterestNet(args, dataset).to(device)
    elif algo == "GRU4REC":
        model = GRU4REC(args, dataset).to(device)
    elif algo == "GRU4REC_movie":
        model = GRU4REC_movie(args, dataset).to(device)
    elif algo == 'DIEN':
        model = DIEN(args, dataset).to(device)
    elif algo == 'DCNv1':
        model = DCN(args, 'v1', dataset).to(device)
    elif algo == 'DCNv2':
        model = DCN(args, 'v2', dataset).to(device)
    elif algo == 'DeepFM':
        model = DeepFM(args, dataset).to(device)
    elif algo == 'xDeepFM':
        model = xDeepFM(args, dataset).to(device)
    elif algo == 'AutoInt':
        model = AutoInt(args, dataset).to(device)
    elif algo == 'FiBiNet':
        model = FiBiNet(args, dataset).to(device)
    elif algo == 'FiGNN':
        model = FiGNN(args, dataset).to(device)
    else:
        print('No Such Model')
        exit()
    model.apply(weight_init)
    return model


def get_optimizer(args, model, train_data_num):
    no_decay = ['bias', 'LayerNorm.weight']
    # no_decay = []
    named_params = [(k, v) for k, v in model.named_parameters()]
    optimizer_grouped_parameters = [
        {
            'params': [p for n, p in named_params if not any(nd in n for nd in no_decay)],
            'weight_decay': args.weight_decay,
        },
        {
            'params': [p for n, p in named_params if any(nd in n for nd in no_decay)],
            'weight_decay': 0.0,
        },
    ]
    beta1, beta2 = args.adam_betas.split(',')
    beta1, beta2 = float(beta1), float(beta2)
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.lr, eps=args.adam_epsilon,
                          betas=(beta1, beta2))
    t_total = int(train_data_num * args.epoch_num)
    t_warmup = int(t_total * args.warmup_ratio)
    if args.lr_sched.lower() == 'cosine':
        scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=t_warmup,
                                                    num_training_steps=t_total)
    elif args.lr_sched.lower() == 'const':
        scheduler = get_constant_schedule_with_warmup(optimizer, num_warmup_steps=t_warmup)
    else:
        raise NotImplementedError
    return optimizer, scheduler


def train(args):
    train_set = AmzDataset(args.data_dir, 'train', args.task, args.max_hist_len, args.augment, args.aug_prefix)
    test_set = AmzDataset(args.data_dir, 'test', args.task, args.max_hist_len, args.augment, args.aug_prefix)
    train_loader = Data.DataLoader(dataset=train_set, batch_size=args.batch_size, shuffle=True)
    test_loader = Data.DataLoader(dataset=test_set, batch_size=args.batch_size, shuffle=False)
    print('Train data size:', len(train_set), 'Test data size:', len(test_set))

    model = load_model(args, test_set)

    optimizer, scheduler = get_optimizer(args, model, len(train_set))

    save_path = os.path.join(args.save_dir, args.algo + '.pt')
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    best_auc = 0
    global_step = 0
    patience = 0
    for epoch in range(args.epoch_num):
        t = time.time()
        train_loss = []
        model.train()
        for _, data in enumerate(train_loader):
            outputs = model(data)
            loss = outputs['loss']
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()
            train_loss.append(loss.item())
            global_step += 1
        train_time = time.time() - t
        eval_auc, eval_ll, eval_loss, eval_time = eval(model, test_loader)
        print("EPOCH %d  STEP %d train loss: %.5f, train time: %.5f, test loss: %.5f, test time: %.5f, auc: %.5f, "
              "logloss: %.5f" % (epoch, global_step, np.mean(train_loss), train_time, eval_loss,
                                 eval_time, eval_auc, eval_ll))
        if eval_auc > best_auc:
            best_auc = eval_auc
            torch.save(model, save_path)
            print('model save in', save_path)
            patience = 0
        else:
            patience += 1
            if patience >= args.patience:
                break


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default='../data/amz/proc_data/')
    parser.add_argument('--save_dir', default='../model/amz/')
    parser.add_argument('--reload_path', type=str, default='', help='model ckpt dir')
    parser.add_argument('--setting_path', type=str, default='', help='setting dir')

    parser.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu', type=str, help='device')
    parser.add_argument('--seed', default=1234, type=int, help='random seed')
    parser.add_argument('--output_dim', default=1, type=int, help='output_dim')
    parser.add_argument('--timestamp', type=str, default=datetime.datetime.now().strftime("%Y%m%d%H%M"))

    parser.add_argument('--epoch_num', default=20, type=int, help='epochs of each iteration.') #
    parser.add_argument('--batch_size', default=512, type=int, help='batch size')
    parser.add_argument('--lr', default=1e-4, type=float, help='learning rate')  #1e-3
    parser.add_argument('--weight_decay', default=0, type=float, help='l2 loss scale')  #0
    parser.add_argument('--adam_betas', default='0.9,0.999', type=str, help='beta1 and beta2 for Adam optimizer.')
    parser.add_argument('--adam_epsilon', default=1e-8, type=str, help='Epsilon for Adam optimizer.')
    parser.add_argument('--lr_sched', default='cosine', type=str, help='Type of LR schedule method')
    parser.add_argument('--warmup_ratio', default=0.0, type=float, help='inear warmup over warmup_ratio if warmup_steps not set')
    parser.add_argument('--dropout', default=0.0, type=float, help='dropout rate')  #0
    parser.add_argument('--convert_dropout', default=0.0, type=float, help='dropout rate of convert module')  # 0
    parser.add_argument('--grad_norm', default=0, type=float, help='max norm of gradient')
    parser.add_argument('--test', action='store_true', help='test mode')
    parser.add_argument('--patience', default=5, type=int, help='The patience for early stop')

    parser.add_argument('--task', default='ctr', type=str, help='task, ctr or rerank')
    parser.add_argument('--algo', default='DIN', type=str, help='model name')
    parser.add_argument('--augment', default='true', type=str, help='whether to use augment vectors')
    parser.add_argument('--aug_prefix', default='chatglm_avg', type=str, help='prefix of augment file')
    parser.add_argument('--convert_type', default='HEA', type=str, help='type of convert module')
    parser.add_argument('--max_hist_len', default=5, type=int, help='the max length of user history')
    parser.add_argument('--embed_dim', default=32, type=int, help='size of embedding')  #32
    parser.add_argument('--final_mlp_arch', default='200,80', type=str2list, help='size of final layer')
    parser.add_argument('--convert_arch', default='128,32', type=str2list,
                        help='size of convert net (MLP/export net in MoE)')
    parser.add_argument('--export_num', default=2, type=int, help='number of expert')
    parser.add_argument('--top_expt_num', default=4, type=int, help='number of expert')
    parser.add_argument('--specific_export_num', default=6, type=int, help='number of specific expert in PLE')
    parser.add_argument('--auxi_loss_weight', default=0, type=float, help='loss for load balance in expert')

    parser.add_argument('--hidden_size', default=64, type=int, help='size of hidden size')
    parser.add_argument('--rnn_dp', default=0.0, type=float, help='dropout rate in RNN')
    parser.add_argument('--dcn_deep_arch', default='200,80', type=str2list, help='size of deep net in DCN')
    parser.add_argument('--dcn_cross_num', default=3, type=int, help='num of cross layer in DCN')
    parser.add_argument('--deepfm_latent_dim', default=16, type=int, help='dimension of latent variable in DeepFM')
    parser.add_argument('--deepfm_deep_arch', default='200,80', type=str2list, help='size of deep net in DeepFM')
    parser.add_argument('--cin_layer_units', default='50,50', type=str2list, help='CIN layer in xDeepFM')
    parser.add_argument('--num_attn_heads', default=1, type=int, help='num of attention head in AutoInt')
    parser.add_argument('--attn_size', default=64, type=int, help='attention size in AutoInt')
    parser.add_argument('--num_attn_layers', default=3, type=int, help='attention layer in AutoInt')
    parser.add_argument('--res_conn', default=True, type=bool, help='residual connection in AutoInt/FiGNN')
    parser.add_argument('--attn_scale', default=True, type=bool, help='attention scale in AutoInt')
    parser.add_argument('--reduction_ratio', default=0.5, type=float, help='reduction_ratio in FiBiNet')
    parser.add_argument('--bilinear_type', default='field_all', type=str, help='bilinear_type in FiBiNet')
    parser.add_argument('--gnn_layer_num', default=2, type=int, help='layer num of GNN in FiGNN')
    parser.add_argument('--reuse_graph_layer', default=True, type=bool, help='whether reuse graph layer in FiGNN')
    parser.add_argument('--dien_gru', default='GRU', type=str, help='gru type in DIEN')

    args, _ = parser.parse_known_args()
    args.augment = True if args.augment.lower() == 'true' else False

    print('max hist len', args.max_hist_len)

    return args


if __name__ == '__main__':
    args = parse_args()
    print(args.timestamp)
    if args.setting_path:
        args = load_parse_from_json(args, args.setting_path)
    setup_seed(args.seed)

    print('parameters', args)
    train(args)

