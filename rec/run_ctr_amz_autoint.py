import subprocess
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# Training fs
data_dir = '../data/amz/proc_data'
task_name = 'ctr'
# dataset_name = 'amz'
dataset_name = 'amz'
aug_prefix = '7b_think_7b_reflect_amz'
augment = True
# augment = True


epoch = 20
batch_size = 256
lr = '5e-4'
lr_sched = 'cosine'
weight_decay = 0  #效果不大

model = 'AutoInt'
# model = 'DIEN'
embed_size = 32
final_mlp = '200,80'
convert_arch = '128,32'
num_cross_layers = 3
dropout = 0.0  #增大会变差

convert_type = 'HEA'
convert_dropout = 0.0
export_num = 2
specific_export_num = 5
dien_gru = 'AIGRU'


# Run the train process

for batch_size in [512,128, 1024,]:
    for lr in ['1e-4','4e-4','5e-4','1e-3','2e-3','4e-3']:
        for embed_size in [32]:
            for specific_export_num in [6]:

                print('---------------bs, lr, epoch, export share/spcf, convert arch, gru----------', batch_size,
                      lr, epoch, export_num, specific_export_num, convert_arch, dien_gru, model)
                subprocess.run(['python', '-u', 'main_ctr.py',
                                f'--save_dir=./model/{dataset_name}/{task_name}/{model}/WDA_Emb{embed_size}_epoch{epoch}'
                                f'_bs{batch_size}_lr{lr}_{convert_arch}'
                                f'_eprt_{export_num}_wd{weight_decay}_drop{dropout}' + \
                                f'_hl{final_mlp}_cl{num_cross_layers}_augment_{augment}',
                                f'--data_dir={data_dir}',
                                f'--augment={augment}',
                                f'--aug_prefix={aug_prefix}',
                                f'--task={task_name}',
                                f'--convert_arch={convert_arch}',
                                f'--convert_type={convert_type}',
                                f'--convert_dropout={convert_dropout}',
                                f'--epoch_num={epoch}',
                                f'--batch_size={batch_size}',
                                f'--lr={lr}',
                                f'--lr_sched={lr_sched}',
                                f'--weight_decay={weight_decay}',
                                f'--algo={model}',
                                f'--embed_size={embed_size}',
                                f'--export_num={export_num}',
                                f'--specific_export_num={specific_export_num}',
                                f'--final_mlp_arch={final_mlp}',
                                f'--dropout={dropout}',
                                f'--dien_gru={dien_gru}'
                                ])
