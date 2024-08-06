# How to load and access a Dataset and an IterableDataset
# https://huggingface.co/docs/datasets/access

# 1. Dataset
from datasets import load_dataset
dataset = load_dataset("rotten_tomatoes", split="train")
# Get the first row in the dataset
# 2. Indexing
print(dataset[0])
# Get the last row in the dataset
print(dataset[-1])
# output:
# {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}
# {'text': 'things really get weird , though not particularly scary : the movie is all portent and no content .', 'label': 0}

# Indexing by the column name returns a list of all the values in the column:
print(dataset["text"])
# output:
"""
['the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .',
 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .',
 'effective but too-tepid biopic',
 ...,
 'things really get weird , though not particularly scary : the movie is all portent and no content .']
"""

# combine row and column name indexing to return a specific value at a position:
print(dataset[0]["text"])
# output:
# the rock is destined to be the 21st century's new " conan " and that he's going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .


import time

start_time = time.time()
text = dataset[0]["text"]
end_time = time.time()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")

start_time = time.time()
text = dataset["text"][0]
end_time = time.time()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")

# output:
# Elapsed time: 0.0001 seconds
# Elapsed time: 0.0049 seconds

# 3. Slicing
# Get the first three rows
print(dataset[:3])
# output:
# {'text': ['the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .', 'effective but too-tepid biopic'], 'label': [1, 1, 1]}

# Get rows between three and six
print(dataset[3:6])
# output:
# {'text': ['if you sometimes like to go to the movies to have fun , wasabi is a good place to start .', "emerges as something rare , an issue movie that's so honest and keenly observed that it doesn't feel like one .", 'the film provides some great insight into the neurotic mindset of all comics -- even those who have reached the absolute top of the game .'], 'label': [1, 1, 1]}

# 4. IterableDataset
# An IterableDataset is loaded when you set the streaming parameter to True in load_dataset():
from datasets import load_dataset
iterable_dataset = load_dataset("food101", split="train", streaming=True)
for example in iterable_dataset:
    print(example)
    break
# output:
# {'image': <PIL.Image.Image image mode=RGB size=384x512 at 0x14E682270>, 'label': 6}

# create an IterableDataset from an existing Dataset：
from datasets import load_dataset
dataset = load_dataset("rotten_tomatoes", split="train")
iterable_dataset = dataset.to_iterable_dataset()
print(next(iter(iterable_dataset)))
# output:
# {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}

for example in iterable_dataset:
    print(example)
    break
# output:
# {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}

# Get first three examples
print(list(iterable_dataset.take(3)))
# output:
# [{'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}, {'text': 'the gorgeously elaborate continuation of " the lord of the rings " trilogy is so huge that a column of words cannot adequately describe co-writer/director peter jackson\'s expanded vision of j . r . r . tolkien\'s middle-earth .', 'label': 1}, {'text': 'effective but too-tepid biopic', 'label': 1}]
