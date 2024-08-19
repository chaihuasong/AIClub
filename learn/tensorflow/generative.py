import tensorflow as tf
from transformers import BertTokenizer

print(tf.config.list_physical_devices('CPU'))
print(tf.config.list_physical_devices('GPU'))

# 假设你的模型保存为 './results/model' 目录下的 'tf_model.h5' 文件

# 加载模型
model = tf.keras.models.load_model('./results/model')

# 加载分词器
tokenizer = BertTokenizer.from_pretrained('./results/tokenizer')

# 准备输入数据
text = "This is a sample sentence for testing."
encoded_input = tokenizer(text, return_tensors='tf')
input_ids = encoded_input['input_ids']
attention_mask = encoded_input['attention_mask']

# 进行预测
with tf.device('/CPU:0'):  # 或者 '/GPU:0' 如果你想在GPU上进行推理
    predictions = model.predict({'input_ids': input_ids, 'attention_mask': attention_mask})

# 处理预测结果
# 这取决于你的模型输出的格式，以下是一个示例，假设模型输出的是概率
predicted_label = tf.argmax(predictions, axis=1).numpy()[0]
print(f"Predicted label: {predicted_label}")

# 如果你的模型输出的是logits，你可能需要将其转换为概率
# predicted_probabilities = tf.nn.softmax(predictions,  axis=1).numpy()
# print(f"Predicted probabilities: {predicted_probabilities}")