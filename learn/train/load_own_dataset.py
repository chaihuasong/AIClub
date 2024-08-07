# https://huggingface.co/docs/datasets/upload_dataset
# https://huggingface.co/datasets/chaihuasong/train_test
from datasets import load_dataset
dataset = load_dataset("chaihuasong/train_test")
print(dataset)
# output:
"""
DatasetDict({
    train: Dataset({
        features: ['image', 'label'],
        num_rows: 3
    })
    test: Dataset({
        features: ['image', 'label'],
        num_rows: 3
    })
})
"""