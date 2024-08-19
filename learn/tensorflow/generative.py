import tensorflow as tf

from transformers import TFBertForSequenceClassification, BertTokenizer

print(tf.config.list_physical_devices('CPU'))
print(tf.config.list_physical_devices('GPU'))

# 加载模型
model = TFBertForSequenceClassification.from_pretrained('./results/model')

# 加载分词器
tokenizer = BertTokenizer.from_pretrained('./results/tokenizer')

# # 准备输入数据
# text = "The Dow Jones Industrial Average climbed 216 points, or 2.1%, to 10,515."
# encoded_input = tokenizer(text, return_tensors='tf')
# input_ids = encoded_input['input_ids']
# attention_mask = encoded_input['attention_mask']
#
# # 进行预测
# with tf.device('/CPU:0'):  # 或者 '/GPU:0' 如果你想在GPU上进行推理
#     outputs = model({'input_ids': input_ids, 'attention_mask': attention_mask})
#
# # 从输出中提取logits
# logits = outputs.logits
#
# # 处理预测结果
# predicted_label = tf.argmax(logits, axis=1).numpy()[0]
# print(f"Predicted label: {predicted_label}")


# 准备输入数据
texts = [
    "The United Nations said Friday that it is 'very close' to a deal with Iran on an investigation into its suspected nuclear weapons program.",
    "USC starts at the top Southern California greeted news of its first preseason No. 1 ranking since 1979 with ambivalence.",
    "The Dow Jones Industrial Average climbed 216 points, or 2.1%, to 10,515.",
    "Open Source Apps Developer SugarCRM Releases Sugar.Sales 1.1 (TechWeb) TechWeb - News - August 13, 2004"
]
encoded_inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='tf')

input_ids = encoded_inputs['input_ids']
attention_mask = encoded_inputs['attention_mask']

# 进行预测
with tf.device('/CPU:0'):  # 或者 '/GPU:0' 如果你想在GPU上进行推理
    outputs = model({'input_ids': input_ids, 'attention_mask': attention_mask})

# 从输出中提取logits
logits = outputs.logits

# 处理预测结果
predicted_labels = tf.argmax(logits, axis=1).numpy()
for i, text in enumerate(texts):
    print(f"Text: {text}\nPredicted label: {predicted_labels[i]}")