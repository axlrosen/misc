import csv
import random
import re
import sys

import Levenshtein


# load our dicts
from collections import Counter, defaultdict

import nltk

LETTERS = re.compile("[^a-z ]")

lines = open("/Users/alex.rosen/personal/xword/corpora/matt-ginsberg-clues.txt", encoding='latin1').readlines()
lines = [line.rstrip().lower().split(",", maxsplit=1)[1] for line in lines]
lines = [LETTERS.sub("", line) for line in lines]
lines = set([line for line in lines if not ("_" in line or "--" in line)])
clues = [line.split() for line in lines]

with open("/Users/alex.rosen/personal/projects/misc/specific/clues-for-ml-experiment.txt", "w") as f:

    words = []
    for clue in clues:
        words.extend(clue)
        print("__label__1 " + " ".join(clue), file = f)

    words = list(words)
    for clue in clues:
        fake_clue = random.choices(words, k=len(clue))
        print("__label__0 " + " ".join(fake_clue), file = f)


