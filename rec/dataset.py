import torch
import torch.utils.data as Data
import pickle
from utils import load_json, load_pickle


class AmzDataset(Data.Dataset):
    def __init__(self, data_path, set='train', task='ctr', max_hist_len=10, augment=False, aug_prefix=None):
        self.task = task
        self.max_hist_len = max_hist_len
        self.augment = augment
        self.set = set
        self.data = load_pickle(data_path + f'/{task}.{set}')
        self.stat = load_json(data_path + '/stat.json')
        self.item_num = self.stat['item_num']
        self.attr_num = self.stat['attribute_num']
        self.attr_ft_num = self.stat['attribute_ft_num']
        self.rating_num = self.stat['rating_num']
        self.dense_dim = self.stat['dense_dim'] # 这里定义了embedding的hidden_size
        if task == 'rerank':
            self.max_list_len = self.stat['rerank_list_len']
        self.length = len(self.data) # 1265059 train_dataset length for example
        self.sequential_data = load_json(data_path + '/sequential_data.json')
        self.item2attribution = load_json(data_path + '/item2attributes.json')
        datamaps = load_json(data_path + '/datamaps.json')
        self.id2item = datamaps['id2item']
        self.id2user = datamaps['id2user']
        if augment:
            self.hist_aug_data = load_json(f'{data_path}/{aug_prefix}_aug.user')
            self.item_aug_data = load_json(f'{data_path}/{aug_prefix}_aug.item')
            # print('item key', list(self.item_aug_data.keys())[:6], len(self.item_aug_data), self.item_num)

    def __len__(self):
        return self.length

    def __getitem__(self, _id):
        if self.task == 'ctr':
            uid, seq_idx, lb = self.data[_id] # user_id seq_idx 和对应的label lb
            item_seq, rating_seq = self.sequential_data[str(uid)]
            iid = item_seq[seq_idx] # seq_idx对应的item
            hist_seq_len = seq_idx - max(0, seq_idx - self.max_hist_len)
            attri_id = self.item2attribution[str(iid)] # seq_idx对应的item对应的attribution
            hist_item_seq = item_seq[max(0, seq_idx - self.max_hist_len): seq_idx] # [3771, 1851, 14495, 10068, 5877, 14370, 86, 10493, 3334, 15321] 去预测 5854
            hist_rating_seq = rating_seq[max(0, seq_idx - self.max_hist_len): seq_idx]
            hist_attri_seq = [self.item2attribution[str(idx)] for idx in hist_item_seq]
            out_dict = {
                'iid': torch.tensor(iid).long(), # target item的id
                'aid': torch.tensor(attri_id).long(), # target item的attribution
                'lb': torch.tensor(lb).long(), # 真实的label
                'hist_iid_seq': torch.tensor(hist_item_seq).long(), # 历史item 的id
                'hist_aid_seq': torch.tensor(hist_attri_seq).long(), # 历史item 的attribution
                'hist_rate_seq': torch.tensor(hist_rating_seq).long(), # 历史item 的分数
                'hist_seq_len': torch.tensor(hist_seq_len).long() # 历史序列的长度
            }
            if self.augment:
                if str(iid) in self.item_aug_data:
                    item_aug_vec = self.item_aug_data[str(iid)]
                else:
                    item_aug_vec = [0.0] * self.dense_dim
                if str(uid) in self.hist_aug_data:
                    hist_aug_vec = self.hist_aug_data[str(uid)]
                else:
                    hist_aug_vec = [0.0] * self.dense_dim
                out_dict['item_aug_vec'] = torch.tensor(item_aug_vec).float()
                out_dict['hist_aug_vec'] = torch.tensor(hist_aug_vec).float()
        elif self.task == 'rerank':
            uid, seq_idx, candidates, candidate_lbs = self.data[_id]
            candidates_attr = [self.item2attribution[str(idx)] for idx in candidates]
            item_seq, rating_seq = self.sequential_data[str(uid)]
            hist_seq_len = seq_idx - max(0, seq_idx - self.max_hist_len)
            hist_item_seq = item_seq[max(0, seq_idx - self.max_hist_len): seq_idx]
            hist_rating_seq = rating_seq[max(0, seq_idx - self.max_hist_len): seq_idx]
            hist_attri_seq = [self.item2attribution[str(idx)] for idx in hist_item_seq]
            out_dict = {
                'iid_list': torch.tensor(candidates).long(),
                'aid_list': torch.tensor(candidates_attr).long(),
                'lb_list': torch.tensor(candidate_lbs).long(),
                'hist_iid_seq': torch.tensor(hist_item_seq).long(),
                'hist_aid_seq': torch.tensor(hist_attri_seq).long(),
                'hist_rate_seq': torch.tensor(hist_rating_seq).long(),
                'hist_seq_len': torch.tensor(hist_seq_len).long()
            }
            if self.augment:
                item_aug_vec = [torch.tensor(self.item_aug_data[str(self.id2item[str(idx)])]).float()
                                for idx in candidates]
                hist_aug_vec = self.hist_aug_data[str(self.id2user[str(uid)])]
                out_dict['item_aug_vec_list'] = item_aug_vec
                out_dict['hist_aug_vec'] = torch.tensor(hist_aug_vec).float()
        else:
            raise NotImplementedError

        return out_dict


