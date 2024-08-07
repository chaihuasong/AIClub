# https://huggingface.co/docs/datasets/upload_dataset
# Upload with Python
# 1. Begin by installing the library:
# pip install huggingface_hub

# 2. To upload a dataset on the Hub in Python, you need to log in to your Hugging Face account:
# huggingface-cli login

# 3. Use the push_to_hub() function to help you add, commit, and push a file to your repository:
from datasets import load_dataset

dataset = load_dataset("stevhliu/demo")
# dataset = dataset.map(...)  # do all your processing here
dataset.push_to_hub("stevhliu/processed_demo")

# set your dataset as private and push
dataset.push_to_hub("stevhliu/private_processed_demo", private=True)

# Privacy
# Load a private dataset by providing your authentication token to the token parameter:
from datasets import load_dataset

# Load a private individual dataset
dataset = load_dataset("stevhliu/demo", token=True)

# Load a private organization dataset
dataset = load_dataset("organization/dataset_name", token=True)