from transformers import AutoModelForSequenceClassification, AutoTokenizer 
import torch 
 
# 确保路径指向包含模型文件的文件夹 
model_folder_path = './saved_model/'
 
# 加载模型和分词器 
model = AutoModelForSequenceClassification.from_pretrained(model_folder_path) 
tokenizer = AutoTokenizer.from_pretrained(model_folder_path) 

# ======== 单句标签开始===========
# 准备输入数据 
# input_text = "The United Nations said Friday that it is 'very close' to a deal with Iran on an investigation into its suspected nuclear weapons program."
# input_text = "The Dow Jones Industrial Average climbed 216 points, or 2.1%, to 10,515."
# input_text = "Open Source Apps Developer SugarCRM Releases Sugar.Sales 1.1 (TechWeb) TechWeb - News - August 13, 2004"

# input_ids = tokenizer.encode(input_text,  return_tensors='pt', truncation=True, padding=True)


# # 进行推理 
# outputs = model(input_ids)
 
# # 获取logits 
# logits = outputs.logits  
 
# # 如果模型有多个标签，将logits转换为概率 
# probabilities = torch.nn.functional.softmax(logits,  dim=1)
 
# # 获取最高概率的标签索引 
# predicted_class_idx = probabilities.argmax().item()

 
# # 如果模型有标签映射，可以使用它来获取标签 
# # label_list = model.config.id2label.values()   # 如果模型配置中有标签映射 
# # predicted_label = label_list[predicted_class_idx]
 
# # 打印预测的标签索引（或标签）
# print(f"Predicted class indices: {predicted_class_idx}")
# # print(f"Predicted label: {predicted_label}")
# ======== 单句标签结束===========


input_texts = [
    "The United Nations said Friday that it is 'very close' to a deal with Iran on an investigation into its suspected nuclear weapons program.",
    "USC starts at the top Southern California greeted news of its first preseason No. 1 ranking since 1979 with ambivalence.",
    "The Dow Jones Industrial Average climbed 216 points, or 2.1%, to 10,515.",
    "Open Source Apps Developer SugarCRM Releases Sugar.Sales 1.1 (TechWeb) TechWeb - News - August 13, 2004"
]
input_ids = tokenizer(input_texts, return_tensors='pt', padding=True, truncation=True)

# 进行推理 
outputs = model(**input_ids)
 
# 获取logits 
logits = outputs.logits  
 
# 如果模型有多个标签，将logits转换为概率 
probabilities = torch.nn.functional.softmax(logits,  dim=1)

# 获取每个文本的预测类别索引 
predicted_class_indices = probabilities.argmax(dim=1).tolist() 
# 获取概率最高的类别的概率值 
predicted_probabilities = probabilities.max(dim=1).values.tolist() 

print(predicted_class_indices)

# 打印预测的类别索引和概率 
for i, (index, prob) in enumerate(zip(predicted_class_indices, predicted_probabilities)):
    print(f"Sample {i+1}: Predicted class index: {index}, Probability: {prob}")