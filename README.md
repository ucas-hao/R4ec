# R4ec
Code for $R^{4}$ec: a \underline{R}easoning,\underline{R}eflection, and \underline{R}efinement framework for \underline{R}ecommendation Systems

### step 1: preprocess dataset
you can first download Amazon-Books dataset and run `python preprocess/preprocess_amz.py` to preprocess Amazon-Books for CTR task.

### step 2: preprocess thinking, reflection, refinement dataset
you can find all prompt template in `prompt/prompt.py`

### step 3: fine-tune actor model and reflection model
we use amz user as a example.
#### step 3.1 download llama_factory
```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```
#### fine-tune amz user actor model and reflection model
```bash
CUDA_VISIBLE_DEVICES=0 llamafactory-cli train examples/train_lora/qwen2.5_7b_amz_user_thinking.yaml
CUDA_VISIBLE_DEVICES=1 llamafactory-cli train examples/train_lora/qwen2.5_7b_amz_user_reflection.yaml
```
you can find qwen2.5_7b_amz_user_thinking.yaml and qwen2.5_7b_amz_user_reflection.yaml in `utils`
