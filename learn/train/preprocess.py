# Tokenize a text dataset.
# Resample an audio dataset.
# Apply transforms to an image dataset.
# https://huggingface.co/docs/datasets/use_dataset

# pip install transformers

# Tokenize text
# 1. Start by loading the rotten_tomatoes dataset and the tokenizer corresponding to a pretrained BERT model.
# Using the same tokenizer as the pretrained model is important because you want to make sure the text is split in the same way.
from transformers import AutoTokenizer, DataCollatorWithPadding
from datasets import load_dataset

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
dataset = load_dataset("rotten_tomatoes", split="train")

print(dataset)
# output:
"""
Dataset({
    features: ['text', 'label'],
    num_rows: 8530
})
"""

# 2. Call your tokenizer on the first row of text in the dataset:
print(tokenizer(dataset[0]["text"]))
# output:
# {'input_ids': [101, 1996, 2600, 2003, 16036, 2000, 2022, 1996, 7398, 2301, 1005, 1055, 2047, 1000, 16608, 1000, 1998, 2008, 2002, 1005, 1055, 2183, 2000, 2191, 1037, 17624, 2130, 3618, 2084, 7779, 29058, 8625, 13327, 1010, 3744, 1011, 18856, 19513, 3158, 5477, 4168, 2030, 7112, 16562, 2140, 1012, 102], 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}

# 3. The fastest way to tokenize your entire dataset is to use the map() function.
# This function speeds up tokenization by applying the tokenizer to batches of examples instead of individual examples. Set the batched parameter to True:
def tokenization(example):
    return tokenizer(example["text"])

dataset = dataset.map(tokenization, batched=True)
print(dataset)
# output:
"""
Dataset({
    features: ['text', 'label', 'input_ids', 'token_type_ids', 'attention_mask'],
    num_rows: 8530
})
"""

# 4. Set the format of your dataset to be compatible with your machine learning framework:
# pip install torch
dataset.set_format(type="torch", columns=["input_ids", "token_type_ids", "attention_mask", "label"])
print(dataset.format['type'])
# output:
"""
{'input_ids': [101, 1996, 2600, 2003, 16036, 2000, 2022, 1996, 7398, 2301, 1005, 1055, 2047, 1000, 16608, 1000, 1998, 2008, 2002, 1005, 1055, 2183, 2000, 2191, 1037, 17624, 2130, 3618, 2084, 7779, 29058, 8625, 13327, 1010, 3744, 1011, 18856, 19513, 3158, 5477, 4168, 2030, 7112, 16562, 2140, 1012, 102], 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
Dataset({
    features: ['text', 'label', 'input_ids', 'token_type_ids', 'attention_mask'],
    num_rows: 8530
})
"""

# from transformers import DataCollatorWithPadding
# pip install tensorflow
data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="tf")
tf_dataset = dataset.to_tf_dataset(
    columns=["input_ids", "token_type_ids", "attention_mask"],
    label_cols=["label"],
    batch_size=2,
    collate_fn=data_collator,
    shuffle=True
)
print(tf_dataset)
# output:
# <_PrefetchDataset element_spec=({'input_ids': TensorSpec(shape=(None, None), dtype=tf.int64, name=None), 'token_type_ids': TensorSpec(shape=(None, None), dtype=tf.int64, name=None), 'attention_mask': TensorSpec(shape=(None, None), dtype=tf.int64, name=None)}, TensorSpec(shape=(None,), dtype=tf.int64, name=None))>

# 5. The dataset is now ready for training with your machine learning framework!


# Resample audio signals
# 1. Start by loading the MInDS-14 dataset, the Audio feature, and the feature extractor corresponding to a pretrained Wav2Vec2 model
from transformers import AutoFeatureExtractor
from datasets import load_dataset, Audio

feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")
dataset = load_dataset("PolyAI/minds14", "en-US", split="train")
print(dataset)
# output: !!!An error occurred while generating the dataset

# 2. Index into the first row of the dataset. When you call the audio column of the dataset, it is automatically decoded and resampled:
print(dataset[0]["audio"])

# 3. Reading a dataset card
dataset = dataset.cast_column("audio", Audio(sampling_rate=16_000))
dataset[0]["audio"]

# 4. Use the map() function
def preprocess_function(examples):
    audio_arrays = [x["array"] for x in examples["audio"]]
    inputs = feature_extractor(
        audio_arrays, sampling_rate=feature_extractor.sampling_rate, max_length=16000, truncation=True
    )
    return inputs

dataset = dataset.map(preprocess_function, batched=True)

# 5. The dataset is now ready for training with your machine learning framework!