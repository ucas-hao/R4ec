# use BERT/chatGLM to encode the knowledge generated by LLM
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import json
# import sys
# sys.path.append('/root/miniconda3/lib/python3.12/site-packages')
import torch
from tqdm import tqdm
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModel
from FlagEmbedding import BGEM3FlagModel
from utils import save_json, get_paragraph_representation
device = 'cuda'

def load_data(path):
    res = []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for id, value in data.items():
            res.append([id, value])
    # print(len(data))
    return res


def get_history_text(data_path):
    raw_data = load_data(data_path)
    idx_list, hist_text = [], []
    for piece in raw_data:
        idx, user_knowledge = piece
        hist_text.append(user_knowledge)
        idx_list.append(idx)
    return idx_list, hist_text


def get_item_text(data_path):
    raw_data = load_data(data_path)
    idx_list, text_list = [], []
    for piece in raw_data:
        iid, item_knowledge = piece
        text_list.append(item_knowledge)
        idx_list.append(iid)
    return idx_list, text_list


def get_text_data_loader(data_path, model_size, batch_size):
    hist_idxes, history = get_history_text(f'{data_path}/7b_think_7b_reflect_movie_user.json')
    print('hist 1', history[1], 'hist len', len(history))
    item_idxes, items = get_item_text(f'{data_path}/7b_think_7b_reflect_movie_item.json')
    print('item 1', items[1], 'item len', len(items))

    history_loader = DataLoader(history, batch_size, shuffle=False)
    item_loader = DataLoader(items, batch_size, shuffle=False)
    return history_loader, hist_idxes, item_loader, item_idxes


def remap_hist(item_idxes,block_idxes, item_vec):
    item_vec_map = {}
    for idx, block_id,vec in zip(item_idxes, block_idxes, item_vec):
        if idx not in item_vec_map:
            item_vec_map[idx] = {}
        item_vec_map[idx][block_id] = vec
    return item_vec_map

def remap_item(item_idxes, item_vec):
    item_vec_map = {}
    for idx, vec in zip(item_idxes, item_vec):
        item_vec_map[idx] = vec
    return item_vec_map

def inference(model, tokenizer, dataloader, model_name, aggregate_type):
    pred_list = []
    if model_name != 'bge':
        model.eval()
    with torch.no_grad():
        for x in tqdm(dataloader):
            torch.cuda.empty_cache()
            if model_name == 'chatglm' or model_name == 'chatglm2':
                x = tokenizer(x, padding=True, truncation=True, return_tensors="pt",
                              return_attention_mask=True).to(device)
                mask = x['attention_mask']
                x.pop('attention_mask')
                outputs = model.transformer(**x, output_hidden_states=True, return_dict=True)
                outputs.last_hidden_state = outputs.last_hidden_state.transpose(1, 0)
            elif model_name == 'longformer':
                x = tokenizer(x, padding=True, truncation=True, max_length=4096, return_tensors="pt",
                              return_attention_mask=True).to(device)
                mask = x['attention_mask']
                outputs = model(**x, output_hidden_states=True, return_dict=True)
            elif model_name == 'bge':
                outputs = model.encode(x, max_length=2048,)['dense_vecs']
            else:
                x = tokenizer(x, padding=True, truncation=True, max_length=512, return_tensors="pt",
                              return_attention_mask=True).to(device)
                mask = x['attention_mask']
                outputs = model(**x, output_hidden_states=True, return_dict=True)
            if model_name == 'bge':
                pred_list.extend(outputs.tolist())
            else:
                pred = get_paragraph_representation(outputs, mask, aggregate_type)
                pred_list.extend(pred.tolist())
    return pred_list


def main(knowledge_path, embedding_path, model_size, model_name, batch_size, aggregate_type):
    hist_loader, hist_idxes, item_loader, item_idxes = get_text_data_loader(knowledge_path, model_size, batch_size)

    if model_name == 'chatglm':
        checkpoint = '../llm/chatglm-6b'
    elif model_name == 'chatglm2':
        checkpoint = '../llm/chatglm-v2'
    elif model_name == 'bert':
        checkpoint = '../llm/bert_base_uncased'
    elif model_name == 'longformer':
        checkpoint = '../llm/longformer_base_4096'
    elif model_name == 'bge':
        checkpoint = '../llm/bge_m3'
    else:
        raise NotImplementedError

    torch.cuda.empty_cache()
    tokenizer = AutoTokenizer.from_pretrained(checkpoint,  trust_remote_code=True)
    if model_name == 'bge':
        model = BGEM3FlagModel(checkpoint, use_fp16=True)
    else:
        model = AutoModel.from_pretrained(checkpoint,  trust_remote_code=True).half().cuda()

    item_vec = inference(model, tokenizer, item_loader, model_name, aggregate_type)
    hist_vec = inference(model, tokenizer, hist_loader, model_name, aggregate_type)
    item_vec_dict = remap_item(item_idxes, item_vec)
    hist_vec_dict = remap_item(hist_idxes, hist_vec)

    save_json(item_vec_dict, f'{embedding_path}/longformer_movie_aug.item')
    save_json(hist_vec_dict, f'{embedding_path}/longformer_movie_aug.user')


if __name__ == '__main__':
    model_size = '7b'
    knowledge_path = 'your knowledge path'
    embedding_path = 'your embedding path'
    main(knowledge_path, embedding_path, model_size, 'longformer', 16, 'avg')

