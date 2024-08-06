# Load a dataset from the Hub!

# 1. Load a dataset
from datasets import load_dataset_builder

ds_builder = load_dataset_builder("rotten_tomatoes")

# 检查数据集描述
print("Inspect dataset description")
print(ds_builder.info.description)

print("Inspect dataset features")
print(ds_builder.info.features)

# output:{'text': Value(dtype='string', id=None), 'label': ClassLabel(names=['neg', 'pos'], id=None)}

from datasets import load_dataset
dataset = load_dataset("rotten_tomatoes", split="train")

print(dataset)

"""
output:
Dataset({
    features: ['text', 'label'],
    num_rows: 8530
})
"""

# 2. Splits
from datasets import get_dataset_split_names
print(get_dataset_split_names("rotten_tomatoes"))

output:['train', 'validation', 'test']

from datasets import load_dataset
dataset = load_dataset("rotten_tomatoes", split="train")
print(dataset)

"""
output Dataset Object:
Dataset({
    features: ['text', 'label'],
    num_rows: 8530
})
"""

from datasets import load_dataset
dataset = load_dataset("rotten_tomatoes")
print(dataset)

"""
output DatasetDict Object:
DatasetDict({
    train: Dataset({
        features: ['text', 'label'],
        num_rows: 8530
    })
    validation: Dataset({
        features: ['text', 'label'],
        num_rows: 1066
    })
    test: Dataset({
        features: ['text', 'label'],
        num_rows: 1066
    })
})
"""

# 3. Configurations
from datasets import get_dataset_config_names
configs = get_dataset_config_names("PolyAI/minds14")
print(configs)

# output:
# ['cs-CZ', 'de-DE', 'en-AU', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT', 'ko-KR', 'nl-NL', 'pl-PL', 'pt-PT', 'ru-RU', 'zh-CN', 'all']

# 471M!
from datasets import load_dataset
mindsFR = load_dataset("PolyAI/minds14", "fr-FR", split="train")


# 4. Remote code
from datasets import get_dataset_config_names, get_dataset_split_names, load_dataset
c4 = load_dataset("c4", "en", split="train", trust_remote_code=True)
get_dataset_config_names("c4", trust_remote_code=True)
get_dataset_split_names("c4", "en", trust_remote_code=True)


