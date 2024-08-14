import torch
from safetensors.torch import load_file, save_file
from transformers import BertForSequenceClassification, BertTokenizer

# 假设你有一个已经转换好的 safetensors 格式的模型文件 "model.safetensors"
model_path = "/Users/chaihuasong/Documents/AI/code/AIClub/learn/pp/saved_model/model.safetensors"

# 从 safetensors 文件加载模型权重
weights = load_file(model_path)

# 获取模型架构
model_name = 'bert-base-uncased'
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 将权重赋值给模型
model.load_state_dict(weights)

# 设置模型为推理模式
model.eval()

# 加载分词器
tokenizer = BertTokenizer.from_pretrained(model_name)


# 进行推理
texts = [
    "The United Nations said Friday that it is 'very close' to a deal with Iran on an investigation into its suspected nuclear weapons program.",
    "The Dow Jones Industrial Average climbed 216 points, or 2.1%, to 10,515.",
    "Open Source Apps Developer SugarCRM Releases Sugar.Sales 1.1 (TechWeb) TechWeb - News - August 13, 2004"
]

# 使用分词器预处理输入文本
inputs = tokenizer(texts, padding=True, truncation=True, max_length=41, return_tensors="pt")

# 进行推理
with torch.no_grad():
    outputs = model(**inputs)

# 获取预测结果
predicted_labels = torch.argmax(outputs.logits,  dim=-1)
print(f"Predicted labels: {predicted_labels.tolist()}")