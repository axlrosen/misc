import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict


entries_list = open("/Users/alex.rosen/personal/xword/combined/split-peter.txt", encoding='latin1').readlines()




animals = open("/Users/alex.rosen/personal/xword/corpora/animals.txt").read().splitlines()
numbers = ['one', 'two', 'three', 'four', 'five', 'six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety','ahundred']


for line in entries_list:
    x = line.split("/")
    entry = x[0]
    split = x[1]
    if not " " in split: continue
    for animal in animals:
        if entry.startswith(animal) and not split.startswith(animal+" ") and not split.startswith(animal+"s ") and not entry == animal and not entry == animal + "s":
            print(animal, entry, split)