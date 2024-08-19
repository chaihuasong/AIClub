import tensorflow as tf
from transformers import TFBertForSequenceClassification, BertTokenizer
from transformers import DataCollatorWithPadding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from datasets import load_dataset

print("加载数据集...")
# 加载数据集
dataset = load_dataset("ag_news")
print("加载数据集完成")

# 加载预训练模型和分词器
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = TFBertForSequenceClassification.from_pretrained(model_name, num_labels=4)


# 预处理数据集
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=41, padding='max_length')


tokenized_dataset = dataset.map(preprocess_function, batched=True)


# 创建数据集格式化函数
def format_dataset(dataset, tokenizer, max_length=41):
    def gen():
        for ex in dataset:
            yield (
                {
                    "input_ids": ex["input_ids"],
                    "attention_mask": ex["attention_mask"],
                },
                to_categorical(ex["label"], num_classes=4)
            )

    return tf.data.Dataset.from_generator(
        gen,
        ({
             "input_ids": tf.int32,
             "attention_mask": tf.int32
         }, tf.float32),
        ({
             "input_ids": tf.TensorShape([None]),
             "attention_mask": tf.TensorShape([None])
         }, tf.TensorShape([4]))
    )


# 创建训练和验证数据集
train_dataset = format_dataset(tokenized_dataset['train'], tokenizer).shuffle(100).batch(8)
val_dataset = format_dataset(tokenized_dataset['test'], tokenizer).batch(8)

# 创建数据集的DataCollator
data_collator = DataCollatorWithPadding(tokenizer)

# 编译模型
optimizer = Adam(learning_rate=5e-5)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("开始训练...")
# 训练模型
history = model.fit(train_dataset, validation_data=val_dataset, epochs=3)
print("训练完成")

# 保存模型
model.save_pretrained('./results/model')  # 保存模型结构和权重
tokenizer.save_pretrained('./results/tokenizer')  # 保存分词器

print("模型已保存到 './results/' 目录下")