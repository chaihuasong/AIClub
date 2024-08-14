# Load model directly
from transformers import BertModel, BertTokenizer

tokenizer = BertTokenizer.from_pretrained("cross-encoder/ms-marco-TinyBERT-L-2-v2")
model = BertModel.from_pretrained("cross-encoder/ms-marco-TinyBERT-L-2-v2")

# 准备输入文本
text = "这是一个例子"

inputs = tokenizer(text, return_tensors='pt')
outputs = model(**inputs)

embeddings = outputs.last_hidden_state
print(embeddings)

print(embeddings.shape)