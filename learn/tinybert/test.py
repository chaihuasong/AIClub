import torch
from safetensors.torch import load_file, save_file
from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# 加载数据集
dataset = load_dataset("ag_news")

# 加载预训练模型和分词器
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=4)  # 保证类别数量正确


# 预处理数据集
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=41, padding='max_length')


encoded_dataset = dataset.map(preprocess_function, batched=True)

# 创建训练和验证数据集
train_dataset = encoded_dataset['train']
val_dataset = encoded_dataset['test']

# 设置训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy='epoch',
    logging_dir='./logs',
    logging_steps=100,
    save_strategy='epoch',
    learning_rate=2e-5,
    weight_decay=0.01,
)

# 创建 Trainer 对象
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# 开始训练
trainer.train()

# 保存模型
model.save_pretrained('./saved_model')
tokenizer.save_pretrained('./saved_model')

# 将模型权重保存为 safetensors 格式
save_file(model.state_dict(), './saved_model/model.safetensors')

# 加载 safetensors 文件中的模型权重
weights = load_file('./saved_model/model.safetensors')

# 加载模型并设置模型为评估模式
model = BertForSequenceClassification.from_pretrained('./saved_model', num_labels=4)  # 重新加载模型
model.eval()

# 只加载匹配的部分权重
model_state_dict = model.state_dict()
for name, param in weights.items():
    if name in model_state_dict and model_state_dict[name].shape == param.shape:
        model_state_dict[name].copy_(param)

# 验证模型性能
trainer.evaluate()

# 进行推理
texts = [
    "The United Nations said Friday that it is 'very close' to a deal with Iran on an investigation into its suspected nuclear weapons program.",
    "The Dow Jones Industrial Average climbed 216 points, or 2.1%, to 10,515."
]

# 使用分词器预处理输入文本
inputs = tokenizer(texts, padding=True, truncation=True, max_length=41, return_tensors='pt')

# 进行推理
with torch.no_grad():
    outputs = model(**inputs)

# 获取预测结果
predicted_labels = torch.argmax(outputs.logits, dim=-1)
print(f"Predicted labels: {predicted_labels.tolist()}") 