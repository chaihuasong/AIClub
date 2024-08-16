import torch
from safetensors.torch import load_file as safeload, save_file as safsave
from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# 加载数据集
dataset = load_dataset("ag_news")

# 加载预训练模型和分词器
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=4).to(device)


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
    eval_steps=10,
    save_steps=1000,
    logging_dir='./logs',
    logging_steps=100,
    save_total_limit=2,
    learning_rate=2e-5,
    weight_decay=0.01
)


# 创建 Trainer 对象
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)


print("开始训练...")
# 开始训练
trainer.train()

print("训练完成...")
# 保存模型
model.save_pretrained('./saved_model')
tokenizer.save_pretrained('./saved_model')

print("保存模型完成...")

# # 加载 safetensors 文件中的模型权重
# try:
#     weights = safeload('./saved_model/model.safetensors')
# except Exception as e:
#     print(f"Error loading safetensors: {e}") 
#     # Handle the error appropriately (e.g., exit, use default weights)

# print("加载 safetensors 文件中的模型权重完成...")

# 只加载匹配的部分权重
#model.load_state_dict(weights)

# 评估模型性能
#result = trainer.evaluate()
#print(f"Evaluation results: {result}") 

# # 进行预测
# text = [
#     "The United Nations said Friday that it is 'very close' to a deal with Iran on an investigation into its suspected nuclear weapons program.",
#     "The Dow Jones Industrial Average climbed 216 points, or 2.1%, to 10,515."
# ]

# # 使用分词器预处理输入文本
# inputs = tokenizer(text, padding=True, truncation=True, max_length=41, return_tensors="pt")

# # 进行预测
# with torch.no_grad():
#     outputs = model(**inputs)

# print(f"Output logits shape: {len(outputs)}")
# # 获取预测结果
# predicted_labels = [torch.argmax(output, dim=-1) for output in outputs]

# print(f"Predicted labels: {predicted_labels}")