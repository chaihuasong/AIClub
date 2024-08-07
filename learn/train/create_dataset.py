# https://huggingface.co/docs/datasets/create_dataset
# Create a dataset
from datasets import load_dataset, Audio

dataset = load_dataset("imagefolder", data_dir="/Users/chaihuasong/Documents/AI/code/AIClub/learn/data")
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

# An audio dataset is created in the same way
# from datasets import load_dataset

# dataset = load_dataset("audiofolder", data_dir="/path/to/folder")

# from_generator()
from datasets import Dataset
def gen():
    yield {"pokemon": "bulbasaur", "type": "grass"}
    yield {"pokemon": "squirtle", "type": "water"}
ds = Dataset.from_generator(gen)
print(ds[0])
# output:
# {'pokemon': 'bulbasaur', 'type': 'grass'}

#  IterableDataset
from datasets import IterableDataset
ds = IterableDataset.from_generator(gen)
for example in ds:
    print(example)
# output:
# {'pokemon': 'bulbasaur', 'type': 'grass'}
# {'pokemon': 'squirtle', 'type': 'water'}


# from_dict()
from datasets import Dataset
ds = Dataset.from_dict({"pokemon": ["bulbasaur", "squirtle"], "type": ["grass", "water"]})
print(ds[0])
# output:
# {'pokemon': 'bulbasaur', 'type': 'grass'}

audio_dataset = Dataset.from_dict({"audio": ["path/to/audio_1", "path/to/audio_n"]}).cast_column("audio", Audio())
print(audio_dataset)
# output:
"""
Dataset({
    features: ['audio'],
    num_rows: 2
})
"""