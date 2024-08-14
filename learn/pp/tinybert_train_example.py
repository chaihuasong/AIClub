from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments
import torch
from datasets import load_dataset

# 加载预训练模型和分词器 
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 准备数据集
dataset = load_dataset('ag_news', split='train')


# 定义预处理函数，确保输入的序列长度为41
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=41, padding='max_length')


# 使用预处理函数处理数据
dataset = dataset.map(preprocess_function, batched=True)

# 设置训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    learning_rate=2e-5,
    weight_decay=0.01,
)

# 创建 Trainer 对象
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset.shard(index=0, num_shards=10),  # 使用一部分数据作为验证集
)

# 开始训练 
trainer.train()

# 保存模型 
trainer.save_model('./saved_model')